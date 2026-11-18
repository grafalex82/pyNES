"""Verify cartridge metadata and exact section contents using synthetic files."""

import pytest

from nesfile import NESFile


@pytest.fixture
def make_nes_file(tmp_path):
    # A factory lets each parameterized case choose exact header and section bytes before writing.
    def create_file(header, prg_rom, chr_rom=b"", *, trainer=b"", extra_roms=b""):
        filename = tmp_path / "cartridge.nes"
        filename.write_bytes(header + trainer + prg_rom + chr_rom + extra_roms)
        return filename

    # The factory captures the isolated directory supplied by pytest for this test case.
    return create_file


@pytest.mark.parametrize("flags6, flags7, mapper", [(0x00, 0x00, 0), (0xA0, 0xB0, 0xBA), (0xF0, 0xF0, 0xFF)])
def test_loads_ines_metadata(make_nes_file, flags6, flags7, mapper):
    # iNES bytes 8 and 9 describe RAM and TV metadata, not extended mapper or ROM sizes.
    header = b"NES\x1a" + bytes([2, 3, flags6, flags7, 1, 1]) + bytes(6)
    prg = b"\x91" * 32768
    chr_rom = b"\x6c" * 24576
    filename = make_nes_file(header, prg, chr_rom)

    # Parse the filename without constructing a machine or selecting a mapper device.
    cartridge = NESFile(str(filename))

    # Preserve all iNES mapper bits, the original header, and the exact ROM sections.
    assert cartridge.get_format() == "iNES"
    assert cartridge.get_header() == header
    assert cartridge.get_mapper() == mapper
    assert cartridge.get_submapper() == 0
    assert cartridge.get_trainer() == b""
    assert cartridge.get_prg_rom() == prg
    assert cartridge.get_chr_rom() == chr_rom


@pytest.mark.parametrize(
    "flags6, flags7, byte8, mapper, submapper",
    [(0x00, 0x08, 0x00, 0, 0), (0x50, 0x68, 0xBA, 0xA65, 0x0B), (0xF0, 0xF8, 0xFF, 0xFFF, 0x0F)],
)
def test_loads_nes20_metadata(make_nes_file, flags6, flags7, byte8, mapper, submapper):
    # NES 2.0 byte 8 splits into mapper and submapper; byte 15 may declare an expansion device.
    header = b"NES\x1a" + bytes([1, 2, flags6, flags7, byte8]) + bytes(6) + b"\x01"
    prg = b"\x35" * 16384
    chr_rom = b"\xa7" * 16384
    filename = make_nes_file(header, prg, chr_rom)

    # Load a Path directly, as callers may already use pathlib for local files.
    cartridge = NESFile(filename)

    # Preserve the extended mapper, independent submapper, and uninterpreted header fields.
    assert cartridge.get_format() == "NES 2.0"
    assert cartridge.get_header() == header
    assert cartridge.get_mapper() == mapper
    assert cartridge.get_submapper() == submapper
    assert cartridge.get_trainer() == b""
    assert cartridge.get_prg_rom() == prg
    assert cartridge.get_chr_rom() == chr_rom


@pytest.mark.parametrize("byte9, prg_count, chr_count", [(0x01, 258, 3), (0x10, 2, 259), (0x21, 258, 515)])
def test_nes20_size_extensions(make_nes_file, byte9, prg_count, chr_count):
    # Different high nibbles and low counts expose swapped PRG/CHR extension fields.
    header = b"NES\x1a" + bytes([2, 3, 0, 0x08, 0, byte9]) + bytes(6)
    prg = b"\x12" * (prg_count * 16384)
    chr_rom = b"\xe7" * (chr_count * 8192)
    filename = make_nes_file(header, prg, chr_rom)

    # Both counts must include byte 9 before the boundary between PRG and CHR is located.
    cartridge = NESFile(filename)

    # Exact bytes check the boundary as well as each declared section length.
    assert cartridge.get_header() == header
    assert cartridge.get_prg_rom() == prg
    assert cartridge.get_chr_rom() == chr_rom


@pytest.mark.parametrize("format_marker", [0x00, 0x08], ids=["ines", "nes20"])
@pytest.mark.parametrize("has_trainer", [False, True], ids=["no-trainer", "trainer"])
@pytest.mark.parametrize("chr_count", [0, 1], ids=["no-chr", "chr"])
def test_extracts_sections(make_nes_file, format_marker, has_trainer, chr_count):
    # Distinct byte patterns reveal an incorrect trainer or PRG/CHR offset.
    flags6 = 0x04 if has_trainer else 0
    header = b"NES\x1a" + bytes([1, chr_count, flags6, format_marker]) + bytes(8)
    trainer = bytes(range(256)) * 2 if has_trainer else b""
    prg = bytes(reversed(range(256))) * 64
    chr_rom = b"\x5a" * (chr_count * 8192)
    contents = header + trainer + prg + chr_rom
    filename = make_nes_file(header, prg, chr_rom, trainer=trainer)

    # Missing sections stay empty rather than causing emulated RAM to be allocated.
    cartridge = NESFile(filename)

    # File sections are immutable bytes and loading does not alter the source file.
    assert cartridge.get_header() == header
    assert cartridge.get_trainer() == trainer
    assert cartridge.get_prg_rom() == prg
    assert cartridge.get_chr_rom() == chr_rom
    sections = (cartridge.get_header(), cartridge.get_trainer(), cartridge.get_prg_rom(), cartridge.get_chr_rom())
    assert all(isinstance(section, bytes) for section in sections)
    assert filename.read_bytes() == contents


@pytest.mark.parametrize("format_marker", [0x00, 0x08], ids=["ines", "nes20"])
@pytest.mark.parametrize(
    "flags6, mirroring, battery",
    [
        (0x00, "horizontal", False),
        (0x01, "vertical", False),
        (0x08, "four-screen", False),
        (0x09, "four-screen", False),
        (0x02, "horizontal", True),
        (0x03, "vertical", True),
        (0x0A, "four-screen", True),
        (0x0B, "four-screen", True),
    ],
)
def test_reads_header_flags(make_nes_file, format_marker, flags6, mirroring, battery):
    # Bit 3 takes precedence over bit 0 for the conventional four-screen header label.
    header = b"NES\x1a" + bytes([1, 0, flags6, format_marker]) + bytes(8)
    filename = make_nes_file(header, bytes(16384))

    # Flags describe cartridge metadata without allocating memory or configuring video.
    cartridge = NESFile(filename)

    # The nonvolatile-memory flag is independent of the mirroring indication.
    assert cartridge.get_mirroring() == mirroring
    assert cartridge.get_battery() is battery


@pytest.mark.parametrize("format_marker", [0x04, 0x0C])
def test_rejects_unrecognized_format_markers(make_nes_file, format_marker):
    # Mapper bits remain independent of the two bits identifying the cartridge format.
    header = b"NES\x1a" + bytes([1, 1, 0, 0xB0 | format_marker]) + bytes(8)
    filename = make_nes_file(header, bytes(16384), bytes(8192))

    # An unknown marker must identify missing format support rather than fall back to iNES.
    with pytest.raises(NotImplementedError, match=f"format marker 0x{format_marker:02X}"):
        NESFile(filename)


@pytest.mark.parametrize(
    "byte9, prg_field, chr_field, prg_size, chr_size, section",
    [(0x0F, 0x34, 1, 8192, 8192, "PRG-ROM"), (0xF0, 1, 0x30, 16384, 4096, "CHR-ROM")],
)
def test_rejects_nes20_exponent_multiplier_sizes(
    make_nes_file, byte9, prg_field, chr_field, prg_size, chr_size, section
):
    # 0x34 encodes 2**13 PRG bytes and 0x30 encodes 2**12 CHR bytes, below ordinary unit sizes.
    header = b"NES\x1a" + bytes([prg_field, chr_field, 0, 0x08, 0, byte9]) + bytes(6)
    filename = make_nes_file(header, bytes(prg_size), bytes(chr_size))

    # Each size field must be rejected independently and name the affected ROM section.
    with pytest.raises(NotImplementedError, match=f"{section} exponent-multiplier size"):
        NESFile(filename)


@pytest.mark.parametrize("format_marker", [0x00, 0x08], ids=["ines", "nes20"])
@pytest.mark.parametrize("console_type", [1, 2, 3])
def test_rejects_nonstandard_console_types(make_nes_file, format_marker, console_type):
    # Low bits select arcade systems or an extended console; type 3 uses byte 13 in NES 2.0.
    header = bytearray(b"NES\x1a" + bytes([1, 1, 0, format_marker | console_type]) + bytes(8))
    if format_marker == 0x08 and console_type == 3:
        header[13] = 0x03
    if format_marker == 0x08 and console_type == 2:
        header[14] = 3
    extra_roms = bytes(8192 + 32) if console_type == 2 else b""
    filename = make_nes_file(header, bytes(16384), bytes(8192), extra_roms=extra_roms)

    # The diagnostic keeps the declared console code visible instead of treating it as a standard NES.
    with pytest.raises(NotImplementedError, match=f"console type 0x{console_type:02X}"):
        NESFile(filename)


@pytest.mark.parametrize("misc_rom_count", [1, 2, 3])
def test_rejects_nes20_miscellaneous_roms(make_nes_file, misc_rom_count):
    # Byte 14 declares extra ROMs after CHR, which the ordinary three-section reader cannot expose.
    header = b"NES\x1a" + bytes([1, 1, 0, 0x08]) + bytes(6) + bytes([misc_rom_count, 0])
    filename = make_nes_file(header, bytes(16384), bytes(8192), extra_roms=b"\xcc" * (128 * misc_rom_count))

    # Every nonzero declaration must be explicit rather than silently discarding the extra area.
    with pytest.raises(NotImplementedError, match="NES 2.0 miscellaneous ROM areas"):
        NESFile(filename)
