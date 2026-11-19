"""Verify CPU memory routing with loaded synthetic cartridges and no CPU."""

import pytest

from machine import Machine
from nesfile import NESFile
from rom import ROM


@pytest.fixture
def make_cartridge(tmp_path):
    # A factory supplies both ordinary NROM layouts through the real loader interface.
    def create_cartridge(prg_rom, format_marker=0, *, header=None, trainer=b""):
        # Explicit headers describe unsupported configurations while keeping each file structurally valid.
        if header is None:
            header = b"NES\x1a" + bytes([len(prg_rom) // 16384, 1, 0, format_marker]) + bytes(8)
        filename = tmp_path / "cartridge.nes"
        filename.write_bytes(header + trainer + prg_rom + b"\xE7" * 8192)
        cartridge = NESFile(filename)

        # Construction must use loaded data even when the source file is no longer available.
        filename.unlink()
        return cartridge

    # Each test controls the PRG bytes while keeping file parsing independent of Machine.
    return create_cartridge


@pytest.mark.parametrize("window", [0x0000, 0x0800, 0x1000, 0x1800])
@pytest.mark.parametrize("offset", [0x0000, 0x0123, 0x07FF])
def test_ram_aliases_share_one_buffer(make_cartridge, window, offset):
    # Each case writes through a different alias of a boundary or interior RAM byte.
    prg = b"\x91" * 16384
    machine = Machine(make_cartridge(prg))
    machine.write_byte(window + offset, 0xA5)

    # All four windows share the changed byte; every other RAM byte and PRG byte stays intact.
    expected_ram = bytearray(2048)
    expected_ram[offset] = 0xA5
    assert bytes(machine.read_byte(address) for address in range(0x2000)) == bytes(expected_ram) * 4
    assert bytes(machine.read_byte(address) for address in range(0x8000, 0x10000)) == prg * 2


def test_initializes_independent_configurations(make_cartridge):
    # Constructing a second Machine must neither inherit nor clear the first one's RAM.
    cartridge = make_cartridge(bytes(16384))
    first = Machine(cartridge)
    assert bytes(first.read_byte(address) for address in range(2048)) == bytes(2048)
    first.write_byte(0x0000, 0x12)
    first.write_byte(0x07FF, 0xAB)
    second = Machine(cartridge)
    assert bytes(second.read_byte(address) for address in range(2048)) == bytes(2048)
    assert bytes(first.read_byte(address) for address in range(2048)) == b"\x12" + bytes(2046) + b"\xAB"

    # Writes through the second Machine's mirrors leave the first Machine's entire buffer unchanged.
    second.write_byte(0x0800, 0x34)
    second.write_byte(0x1FFF, 0xCD)
    assert bytes(second.read_byte(address) for address in range(2048)) == b"\x34" + bytes(2046) + b"\xCD"
    assert bytes(first.read_byte(address) for address in range(2048)) == b"\x12" + bytes(2046) + b"\xAB"


@pytest.mark.parametrize("format_marker", [0x00, 0x08], ids=["ines", "nes20"])
@pytest.mark.parametrize("prg_size", [16384, 32768])
def test_maps_prg_in_file_order(make_cartridge, format_marker, prg_size):
    # Different 8 KiB regions expose incorrect offsets and accidental mirroring of a 32 KiB image.
    prg = bytes(range(256)) * 32 + b"\x3C" * 8192
    if prg_size == 32768:
        prg += b"\xA5" * 8192 + bytes(reversed(range(256))) * 32
    cartridge = make_cartridge(prg, format_marker)
    header = cartridge.get_header()
    machine = Machine(cartridge)

    # Check the complete CPU window, including both sides of $BFFF/$C000 and the last byte at $FFFF.
    expected = prg * 2 if prg_size == 16384 else prg
    assert bytes(machine.read_byte(address) for address in range(0x8000, 0x10000)) == expected
    assert cartridge.get_header() == header
    assert cartridge.get_prg_rom() == prg
    assert cartridge.get_chr_rom() == b"\xE7" * 8192


@pytest.mark.parametrize("prg_size", [16384, 32768])
@pytest.mark.parametrize("address", [0x8000, 0x9FFF, 0xBFFF, 0xC000, 0xDFFF, 0xFFFF])
def test_rom_write_errors_preserve_rom_and_ram(make_cartridge, prg_size, address):
    # Existing RAM contents make accidental writes or reinitialization observable.
    prg = bytes(range(256)) * (prg_size // 256)
    machine = Machine(make_cartridge(prg))
    machine.write_byte(0x0000, 0x12)
    machine.write_byte(0x07FF, 0xAB)

    # Both differing and already-present byte values must reach the ROM's diagnostic trap.
    offset = (address - 0x8000) % prg_size
    with pytest.raises(PermissionError, match=f"ROM at offset 0x{offset:04X}"):
        machine.write_byte(address, 0xFF)

    # Rejection preserves all ROM bytes and every RAM alias.
    expected_rom = prg * 2 if prg_size == 16384 else prg
    expected_ram = b"\x12" + bytes(2046) + b"\xAB"
    assert bytes(machine.read_byte(address) for address in range(0x8000, 0x10000)) == expected_rom
    assert bytes(machine.read_byte(address) for address in range(0x2000)) == expected_ram * 4


def test_propagates_the_original_rom_exception(make_cartridge, monkeypatch):
    # A specific device exception exposes wrapping or replacement by the routing layer.
    machine = Machine(make_cartridge(bytes(16384)))
    error = PermissionError("ROM device diagnostic")

    def reject_write(self, offset, value):
        raise error

    # Replace the device operation without exposing Machine's private storage to the test.
    monkeypatch.setattr(ROM, "write_byte", reject_write)
    with pytest.raises(PermissionError) as caught:
        machine.write_byte(0xC123, 0xA5)
    assert caught.value is error


@pytest.mark.parametrize("operation", ["read", "write"])
@pytest.mark.parametrize("address", [0x4000, 0x4014, 0x4015, 0x4016, 0x4017, 0x4018, 0x401F, 0x4020, 0x5FFF,
                                     0x6000, 0x7FFF])
def test_rejects_unconnected_access_without_changing_memory(make_cartridge, operation, address):
    # Existing bytes expose accidental routing to RAM or ROM instead of an unconnected device.
    prg = bytes(range(256)) * 64
    machine = Machine(make_cartridge(prg))
    machine.write_byte(0x0000, 0x12)
    machine.write_byte(0x07FF, 0xAB)

    # Unconnected ranges report the operation and CPU address.
    with pytest.raises(NotImplementedError, match=rf"{operation}.*0x{address:04X}"):
        if operation == "read":
            machine.read_byte(address)
        else:
            machine.write_byte(address, 0xA5)

    # Neither rejected operation may alter any mapped byte, including RAM mirrors.
    expected_ram = b"\x12" + bytes(2046) + b"\xAB"
    assert bytes(machine.read_byte(index) for index in range(0x2000)) == expected_ram * 4
    assert bytes(machine.read_byte(index) for index in range(0x8000, 0x10000)) == prg * 2


def test_ppu_writes_route_all_mirrors_and_preserve_other_offsets(make_cartridge):
    # Every CPU address in the window must select exactly one of the eight offsets.
    machine = Machine(make_cartridge(bytes(16384)))
    expected = [None] * 8
    assert machine.ppu.last_writes == tuple(expected)
    for address in range(0x2000, 0x4000):
        value = (address // 8 + address) & 0xFF
        machine.write_byte(address, value)
        expected[address & 7] = value
        assert machine.ppu.last_writes == tuple(expected)


def test_status_writes_through_mirrors_only_retain_the_last_byte(make_cartridge):
    # Give all other register offsets and RAM distinct contents before writing PPUSTATUS.
    prg = bytes(range(256)) * 64
    machine = Machine(make_cartridge(prg))
    machine.write_byte(0x123, 0xA5)
    for offset in range(8):
        if offset != 2:
            machine.write_byte(0x2000 + offset, 0x10 + offset)

    # PPUSTATUS is read-only on hardware; this model records writes without register effects.
    for address, value in ((0x2002, 0x00), (0x200A, 0x80), (0x3FFA, 0xFF)):
        machine.write_byte(address, value)
        assert machine.ppu.last_writes == (0x10, 0x11, value, 0x13, 0x14, 0x15, 0x16, 0x17)
        assert machine.read_byte(0x123) == 0xA5
        assert machine.read_byte(0x8000) == prg[0]

    # Reading status is still unsupported and must not expose or change the retained byte.
    with pytest.raises(NotImplementedError, match="PPU read at register offset 0x02"):
        machine.read_byte(0x2002)
    assert machine.ppu.last_writes[2] == 0xFF


@pytest.mark.parametrize("offset", range(8))
def test_ppu_register_reads_remain_explicitly_unsupported(make_cartridge, offset):
    machine = Machine(make_cartridge(bytes(16384)))
    with pytest.raises(NotImplementedError, match=rf"PPU read at register offset 0x{offset:02X}"):
        machine.read_byte(0x3FF8 + offset)


def test_ppu_reads_route_all_mirrors_to_register_offsets(make_cartridge, monkeypatch):
    # A stand-in read exposes the offset and verifies that Machine returns the device's result.
    machine = Machine(make_cartridge(bytes(16384)))
    monkeypatch.setattr(machine.ppu, "read_byte", lambda offset: 0x80 | offset)
    for address in range(0x2000, 0x4000):
        assert machine.read_byte(address) == 0x80 | (address & 7)


def test_ppu_read_error_reports_register_offset(make_cartridge):
    # Unsupported mirrored reads propagate the PPU's device-relative diagnostic directly.
    machine = Machine(make_cartridge(bytes(16384)))
    with pytest.raises(NotImplementedError, match="PPU read at register offset 0x02"):
        machine.read_byte(0x3FFA)


def test_each_machine_owns_independent_ppu(make_cartridge):
    # Constructing and writing a second Machine cannot change the first PPU's retained bytes.
    cartridge = make_cartridge(bytes(16384))
    first = Machine(cartridge)
    first.write_byte(0x2001, 0xAB)
    second = Machine(cartridge)
    assert second.ppu.last_writes == (None,) * 8
    second.write_byte(0x3FF9, 0xCD)
    assert first.ppu.last_writes[1] == 0xAB
    assert second.ppu.last_writes[1] == 0xCD


@pytest.mark.parametrize(
    "header_fields, trainer_size, feature",
    [
        pytest.param([1, 1, 0x10, 0, 0], 0, "mapper 1", id="ines-low-mapper-bits"),
        pytest.param([1, 1, 0, 0x20, 0], 0, "mapper 32", id="ines-high-mapper-bits"),
        pytest.param([1, 1, 0, 0x08, 1], 0, "mapper 256", id="nes20-extended-mapper"),
        pytest.param([1, 1, 0, 0x08, 0x10], 0, "submapper 1", id="nes20-submapper-1"),
        pytest.param([1, 1, 0, 0x08, 0xF0], 0, "submapper 15", id="nes20-submapper-15"),
        pytest.param([3, 1, 0, 0, 0], 0, "PRG ROM size 49152 bytes", id="ines-48-kib-prg"),
        pytest.param([4, 1, 0, 0x08, 0], 0, "PRG ROM size 65536 bytes", id="nes20-64-kib-prg"),
        pytest.param([1, 1, 0x04, 0, 0], 512, "trainer placement", id="ines-trainer"),
        pytest.param([1, 1, 0x04, 0x08, 0], 512, "trainer placement", id="nes20-trainer"),
    ],
)
def test_rejects_unsupported_cartridge_configurations(make_cartridge, header_fields, trainer_size, feature):
    # Complete file sections match the header; these cases concern unsupported wiring, not damaged input.
    header = b"NES\x1a" + bytes(header_fields) + bytes(7)
    prg = b"\x91" * (header_fields[0] * 16384)
    trainer = b"\x35" * trainer_size
    cartridge = make_cartridge(prg, header=header, trainer=trainer)

    # Loading succeeds before Machine independently rejects the unsupported configuration by name.
    with pytest.raises(NotImplementedError, match=rf"{feature}.*not implemented"):
        Machine(cartridge)

    # Rejection leaves the already parsed cartridge data intact for inspection or later implementation.
    assert cartridge.get_header() == header
    assert cartridge.get_prg_rom() == prg
    assert cartridge.get_trainer() == trainer
    assert cartridge.get_chr_rom() == b"\xE7" * 8192
