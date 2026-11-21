"""Verify the PPU's pattern, nametable, and palette memory with synthetic cartridges."""

import pytest

from cpu import CPU
from machine import Machine
from nesfile import NESFile


@pytest.fixture
def make_machine(tmp_path):
    def create_machine(chr_rom, mirroring=0):
        # The reset vector points to a single SEI instruction in the fixed PRG bank.
        prg = bytearray(16384)
        prg[0] = 0x78
        prg[-4:-2] = b"\x00\x80"
        header = b"NES\x1a" + bytes([1, len(chr_rom) // 8192, mirroring]) + bytes(9)
        path = tmp_path / "pattern.nes"
        path.write_bytes(header + prg + chr_rom)
        return Machine(NESFile(path))

    return create_machine


@pytest.mark.parametrize("address", [0x0000, 0x0FFF, 0x1000, 0x1FFF])
def test_chr_rom_maps_pattern_table_boundaries_and_rejects_writes(make_machine, address):
    # Different edge bytes distinguish the two tables and their order within the cartridge.
    chr_rom = bytearray(8192)
    for offset, value in ((0x0000, 0x12), (0x0FFF, 0x34), (0x1000, 0x56), (0x1FFF, 0x78)):
        chr_rom[offset] = value
    machine = make_machine(chr_rom)
    assert machine.ppu.read_vram(address) == chr_rom[address]

    # A write to ROM fails and leaves the complete pattern data unchanged.
    with pytest.raises(PermissionError, match=rf"ROM at offset 0x{address:04X}"):
        machine.ppu.write_vram(address, 0xFF)
    assert bytes(machine.ppu.read_vram(offset) for offset in range(8192)) == bytes(chr_rom)


def test_ppudata_chr_rom_write_propagates_error_without_advancing(make_machine):
    machine = make_machine(bytes([0x5A]) * 8192)
    machine.write_byte(0x2006, 0x1F)
    machine.write_byte(0x2006, 0xFF)
    with pytest.raises(PermissionError, match="ROM at offset 0x1FFF"):
        machine.write_byte(0x2007, 0xA5)
    assert machine.ppu.read_vram(0x1FFF) == 0x5A
    assert machine.ppu._vram_address == 0x1FFF


@pytest.mark.parametrize("chr_size, feature", [(0, "CHR RAM"), (16384, "CHR ROM size 16384 bytes")])
@pytest.mark.parametrize("operation", ["read", "write"])
def test_unsupported_chr_configurations_fail_only_on_video_access(make_machine, chr_size, feature, operation):
    # The same cartridge can execute PRG code even when its pattern memory is not supported.
    machine = make_machine(bytes(chr_size))
    cpu = CPU(machine)
    cpu.step()
    assert cpu.pc == 0x8001
    assert cpu.interrupt_disable

    # Both CHR reads and writes report the actual unsupported configuration.
    with pytest.raises(NotImplementedError, match=feature):
        if operation == "read":
            machine.ppu.read_vram(0x1000)
        else:
            machine.ppu.write_vram(0x1000, 0xA5)


@pytest.mark.parametrize("mirroring,pages", [(0, (0, 0, 1, 1)), (1, (0, 1, 0, 1))],
                         ids=["horizontal", "vertical"])
@pytest.mark.parametrize("table", range(4))
@pytest.mark.parametrize("offset", [0x000, 0x123, 0x2FF, 0x3FF])
def test_nametable_aliases_share_only_the_selected_physical_page(make_machine, mirroring, pages, table, offset):
    # A write through each logical table must affect its alias but not the other physical page.
    machine = make_machine(bytes(8192), mirroring)
    address = 0x2000 + table * 0x400 + offset
    machine.ppu.write_vram(address, 0xA5)
    for index, page in enumerate(pages):
        expected = 0xA5 if page == pages[table] else 0
        alias = 0x2000 + index * 0x400 + offset
        assert machine.ppu.read_vram(alias) == expected
        if alias < 0x2F00:
            assert machine.ppu.read_vram(alias + 0x1000) == expected

    # Every implemented $3000 mirror is writable and refers to the same underlying byte.
    if address < 0x2F00:
        machine.ppu.write_vram(address + 0x1000, 0x5A)
        assert machine.ppu.read_vram(address) == 0x5A


@pytest.mark.parametrize("mirroring", [0, 1], ids=["horizontal", "vertical"])
def test_nametable_ram_is_independent_of_cpu_ram_and_other_machines(make_machine, mirroring):
    # Two machines start with separate zero-filled video and CPU memory.
    first = make_machine(bytes(8192), mirroring)
    second = make_machine(bytes(8192), mirroring)
    first.write_byte(0x0000, 0x12)
    first.ppu.write_vram(0x2000, 0x34)
    first.ppu.write_vram(0x2FFF, 0x56)
    assert first.read_byte(0x0000) == 0x12
    assert first.ppu.read_vram(0x2000) == 0x34
    assert first.ppu.read_vram(0x2FFF) == 0x56
    assert second.read_byte(0x0000) == 0
    assert second.ppu.read_vram(0x2000) == 0
    assert second.ppu.read_vram(0x2FFF) == 0

    # Writes to the second machine do not change the first machine's memory.
    second.write_byte(0x0000, 0x78)
    second.ppu.write_vram(0x2000, 0x9A)
    assert first.read_byte(0x0000) == 0x12
    assert first.ppu.read_vram(0x2000) == 0x34


@pytest.mark.parametrize("operation", ["read", "write"])
def test_four_screen_mirroring_is_rejected_only_on_nametable_access(make_machine, operation):
    # Unsupported nametable wiring does not prevent CPU execution or CHR reads.
    machine = make_machine(bytes(8192), 0x08)
    cpu = CPU(machine)
    cpu.step()
    assert cpu.pc == 0x8001
    assert machine.ppu.read_vram(0x0000) == 0

    # Do not silently replace cartridge-provided four-screen wiring with two-screen mirroring.
    with pytest.raises(NotImplementedError, match="four-screen"):
        if operation == "read":
            machine.ppu.read_vram(0x2000)
        else:
            machine.ppu.write_vram(0x2000, 0xA5)


@pytest.mark.parametrize("entry", range(32))
@pytest.mark.parametrize("mirror", range(8))
def test_palette_entries_repeat_across_the_full_palette_range(make_machine, entry, mirror):
    # Explicit aliases distinguish the four shared sprite entries from all other colors.
    aliases = {0x10: 0x00, 0x14: 0x04, 0x18: 0x08, 0x1C: 0x0C}
    machine = make_machine(bytes(8192))
    machine.ppu.write_vram(0x3F00 + mirror * 32 + entry, 0xA1)
    selected = aliases.get(entry, entry)

    # Each of the eight 32-byte ranges selects the same entries without changing adjacent colors.
    for address in range(0x3F00, 0x4000):
        candidate = (address - 0x3F00) % 32
        expected = 0x21 if aliases.get(candidate, candidate) == selected else 0
        assert machine.ppu.read_vram(address) == expected


@pytest.mark.parametrize("background,sprite", [(0x00, 0x10), (0x04, 0x14), (0x08, 0x18), (0x0C, 0x1C)])
def test_palette_aliases_share_writes_in_both_directions(make_machine, background, sprite):
    machine = make_machine(bytes(8192))
    machine.ppu.write_vram(0x3F00 + background, 0x12)
    assert machine.ppu.read_vram(0x3F00 + sprite) == 0x12
    machine.ppu.write_vram(0x3F00 + sprite + 0x20, 0xE1)
    assert machine.ppu.read_vram(0x3F00 + background) == 0x21
    assert machine.ppu.read_vram(0x3F00 + background + 0x20) == 0x21


@pytest.mark.parametrize("value,expected", [(0x00, 0x00), (0x3F, 0x3F), (0x40, 0x00),
                                           (0x80, 0x00), (0xE1, 0x21), (0xFF, 0x3F)])
def test_palette_stores_only_six_color_bits(make_machine, value, expected):
    machine = make_machine(bytes(8192))
    machine.ppu.write_vram(0x3FFF, value)
    assert machine.ppu.read_vram(0x3F1F) == expected


def test_palette_is_independent_of_other_memory_and_machines(make_machine):
    # Palette RAM belongs to each PPU and does not alias adjacent nametable memory.
    first = make_machine(bytes(8192))
    second = make_machine(bytes(8192))
    first.ppu.write_vram(0x3EFF, 0xAB)
    first.ppu.write_vram(0x3F00, 0x3F)
    assert first.ppu.read_vram(0x3EFF) == 0xAB
    assert first.ppu.read_vram(0x3F00) == 0x3F
    assert second.ppu.read_vram(0x3F00) == 0

    # Independent writes to another PPU cannot change the first palette.
    second.ppu.write_vram(0x3F10, 0x12)
    assert first.ppu.read_vram(0x3F00) == 0x3F
