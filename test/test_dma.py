"""Verify functional OAM DMA through the CPU memory map."""

import pytest

from emulator import Emulator


def test_dma_copies_mirrored_page_and_wraps_oam(make_cpu, monkeypatch):
    # Fill a physical RAM page with distinct values and select a nonzero OAM address.
    _, machine = make_cpu()
    for offset in range(256):
        machine.write_byte(0x0200 + offset, (offset * 7 + 3) & 0xFF)
    machine.write_byte(0x2003, 0xF0)
    original_read = machine.read_byte
    addresses = []

    def record_read(address):
        addresses.append(address)
        return original_read(address)

    # Page $0A mirrors $02; a complete transfer wraps and restores the starting OAM address.
    monkeypatch.setattr(machine, "read_byte", record_read)
    machine.write_byte(0x4014, 0x0A)
    assert addresses == list(range(0x0A00, 0x0B00))
    assert machine.ppu._oam_address == 0xF0
    for offset in range(256):
        machine.write_byte(0x2003, (0xF0 + offset) & 0xFF)
        assert machine.read_byte(0x2004) == (offset * 7 + 3) & 0xFF
    with pytest.raises(NotImplementedError, match="CPU read at address 0x4014"):
        machine.read_byte(0x4014)


def test_dma_reads_in_order_and_propagates_unimplemented_source(make_cpu, monkeypatch):
    # Record normal Machine reads, including the first unsupported source address.
    _, machine = make_cpu()
    original_read = machine.read_byte
    addresses = []

    def record_read(address):
        addresses.append(address)
        return original_read(address)

    # A failed source read stops the transfer after any earlier successful bytes.
    monkeypatch.setattr(machine, "read_byte", record_read)
    with pytest.raises(NotImplementedError, match="CPU read at address 0x4014"):
        machine.write_byte(0x4014, 0x40)
    assert addresses == list(range(0x4000, 0x4015))


def test_cpu_continues_after_dma_without_stall(make_cpu):
    # LDA #$02; STA $4014; NOP transfers a RAM page during the store instruction.
    _, machine = make_cpu()
    for address, value in enumerate((0xA9, 0x02, 0x8D, 0x14, 0x40, 0xEA)):
        machine.write_byte(address, value)
    machine.write_byte(0x0200, 0xA5)
    emulator = Emulator(machine)

    # Only the instructions' nominal cycles advance the CPU and PPU.
    emulator.step()
    emulator.step()
    emulator.step()
    assert machine.read_byte(0x2004) == 0xA5
    assert emulator.cpu.pc == 0x0006
    assert emulator.cpu.cycles == 8
    assert machine.ppu._frame_cycle == 8
