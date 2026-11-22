"""Verify the temporary controller strobe write stub."""

import pytest

from emulator import Emulator


@pytest.mark.parametrize("value", [0x00, 0x01, 0xFF])
def test_controller_reads_return_zero_after_strobe_writes(make_cpu, value):
    _, machine = make_cpu()
    machine.write_byte(0x4016, value)
    for _ in range(10):
        assert machine.read_byte(0x4016) == 0
        assert machine.read_byte(0x4017) == 0


def test_cpu_continues_after_controller_write(make_cpu):
    # LDA #$01; STA $4016; NOP exercises the strobe write through CPU routing.
    _, machine = make_cpu()
    machine.write_byte(0x0000, 0xA9)
    machine.write_byte(0x0001, 0x01)
    machine.write_byte(0x0002, 0x8D)
    machine.write_byte(0x0003, 0x16)
    machine.write_byte(0x0004, 0x40)
    machine.write_byte(0x0005, 0xEA)
    emulator = Emulator(machine)

    # The next instruction executes with only the ordinary instruction cycles.
    emulator.step()
    emulator.step()
    emulator.step()
    assert emulator.cpu.pc == 0x0006
    assert emulator.cpu.cycles == 8


@pytest.mark.parametrize("address", [0x4016, 0x4017])
def test_cpu_reads_controller_stub(make_cpu, address):
    # LDA absolute reads the selected port and applies the ordinary zero flag.
    _, machine = make_cpu()
    machine.write_byte(0x0000, 0xAD)
    machine.write_byte(0x0001, address & 0xFF)
    machine.write_byte(0x0002, 0x40)
    emulator = Emulator(machine)
    emulator.cpu.a = 0xFF
    emulator.step()
    assert emulator.cpu.a == 0
    assert emulator.cpu.zero is True
    assert emulator.cpu.cycles == 4
