"""Verify offline PRG loading using synthetic mapper-0 cartridges."""

import pytest

from misc.disassemble import load_prg_rom


@pytest.fixture
def make_cartridge_file(tmp_path):
    def create_file(header, prg_rom, *, trainer=b"", chr_rom=b"\xE7" * 8192):
        filename = tmp_path / "cartridge.nes"
        filename.write_bytes(header + trainer + prg_rom + chr_rom)
        return filename

    return create_file


@pytest.mark.parametrize("format_marker", [0x00, 0x08], ids=["ines", "nes20"])
@pytest.mark.parametrize("prg_size, base_address", [(16384, 0xC000), (32768, 0x8000)])
@pytest.mark.parametrize("has_trainer", [False, True], ids=["no-trainer", "trainer"])
def test_loads_prg_in_file_order(make_cartridge_file, format_marker, prg_size, base_address, has_trainer):
    # Different sections and PRG halves expose incorrect offsets or accidental mirroring.
    header = b"NES\x1a" + bytes([prg_size // 16384, 1, 0x04 if has_trainer else 0, format_marker]) + bytes(8)
    trainer = b"\x35" * 512 if has_trainer else b""
    prg_rom = bytes(range(256)) * 64
    if prg_size == 32768:
        prg_rom += bytes(reversed(range(256))) * 64
    filename = make_cartridge_file(header, prg_rom, trainer=trainer)
    original = filename.read_bytes()

    # Loading uses the physical PRG bytes once and selects the corresponding CPU listing window.
    loaded_prg, base = load_prg_rom(filename)
    assert loaded_prg == prg_rom
    assert base == base_address
    assert filename.read_bytes() == original


@pytest.mark.parametrize(
    "flags6, flags7, byte8, prg_banks, message",
    [
        (0x10, 0x00, 0x00, 1, "Cartridge mapper 1"),
        (0x00, 0x10, 0x00, 1, "Cartridge mapper 16"),
        (0x00, 0x08, 0x01, 1, "Cartridge mapper 256"),
        (0x00, 0x08, 0x20, 1, "Mapper 0 submapper 2"),
        (0x00, 0x00, 0x00, 0, "Mapper 0 PRG ROM size 0 bytes"),
        (0x00, 0x00, 0x00, 3, "Mapper 0 PRG ROM size 49152 bytes"),
    ],
)
def test_rejects_unsupported_layouts(make_cartridge_file, flags6, flags7, byte8, prg_banks, message):
    # Distinct header fields exercise each part of the parsed mapper and the supported PRG sizes.
    header = b"NES\x1a" + bytes([prg_banks, 1, flags6, flags7, byte8]) + bytes(7)
    filename = make_cartridge_file(header, bytes(prg_banks * 16384))

    # A parsed but unsupported configuration must identify the missing mapping.
    with pytest.raises(NotImplementedError, match=message):
        load_prg_rom(filename)
