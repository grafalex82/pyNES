"""Verify the temporary OAM DMA write stub."""

import pytest

from emulator import Emulator


@pytest.mark.parametrize("page", [0x00, 0x20, 0x40, 0xFF])
def test_dma_write_is_ignored_and_read_is_unsupported(make_cpu, page):
    # Pages including unsupported CPU reads must not be accessed by the stub.
    _, machine = make_cpu()
    machine.write_byte(0x0000, 0xA5)
    machine.write_byte(0x4014, page)
    assert machine.read_byte(0x0000) == 0xA5
    with pytest.raises(NotImplementedError, match="CPU read at address 0x4014"):
        machine.read_byte(0x4014)


def test_cpu_continues_after_dma_write_without_stall(make_cpu):
    # LDA #$40; STA $4014; NOP selects a page containing unsupported read addresses.
    _, machine = make_cpu()
    machine.write_byte(0x0000, 0xA9)
    machine.write_byte(0x0001, 0x40)
    machine.write_byte(0x0002, 0x8D)
    machine.write_byte(0x0003, 0x14)
    machine.write_byte(0x0004, 0x40)
    machine.write_byte(0x0005, 0xEA)
    emulator = Emulator(machine)

    # Only the instructions' nominal cycles advance the CPU and PPU.
    emulator.step()
    emulator.step()
    emulator.step()
    assert emulator.cpu.pc == 0x0006
    assert emulator.cpu.cycles == 8
    assert machine.ppu._frame_cycle == 8
