"""Verify the PPU's fixed mapper-0 pattern memory with synthetic cartridges."""

import pytest

from cpu import CPU
from machine import Machine
from nesfile import NESFile


@pytest.fixture
def make_machine(tmp_path):
    def create_machine(chr_rom):
        # The reset vector points to a single SEI instruction in the fixed PRG bank.
        prg = bytearray(16384)
        prg[0] = 0x78
        prg[-4:-2] = b"\x00\x80"
        header = b"NES\x1a" + bytes([1, len(chr_rom) // 8192]) + bytes(10)
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
    assert machine.ppu.read_memory(address) == chr_rom[address]

    # A write to ROM fails and leaves the complete pattern data unchanged.
    with pytest.raises(PermissionError, match=rf"ROM at offset 0x{address:04X}"):
        machine.ppu.write_memory(address, 0xFF)
    assert bytes(machine.ppu.read_memory(offset) for offset in range(8192)) == bytes(chr_rom)


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
            machine.ppu.read_memory(0x1000)
        else:
            machine.ppu.write_memory(0x1000, 0xA5)


@pytest.mark.parametrize("operation", ["read", "write"])
def test_other_ppu_memory_is_not_mapped_to_chr(make_machine, operation):
    machine = make_machine(bytes(8192))
    with pytest.raises(NotImplementedError, match=rf"PPU memory {operation}.*0x2000"):
        if operation == "read":
            machine.ppu.read_memory(0x2000)
        else:
            machine.ppu.write_memory(0x2000, 0xA5)
