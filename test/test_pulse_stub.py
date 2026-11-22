"""Verify temporary audio-channel control write stubs."""

import logging

import pytest

from emulator import Emulator


@pytest.mark.parametrize("value", [0x00, 0x7F, 0xFF])
@pytest.mark.parametrize("address", [0x4000, 0x4004, 0x4008, 0x400C])
def test_pulse_control_write_routes_to_apu_and_read_remains_unsupported(make_cpu, monkeypatch, caplog, value, address):
    _, machine = make_cpu()
    writes = []
    original_write = machine.apu.write_byte

    def record_write(offset, byte):
        writes.append((offset, byte))
        original_write(offset, byte)

    # Machine routes the write to the dummy APU, which logs the discarded byte.
    monkeypatch.setattr(machine.apu, "write_byte", record_write)
    with caplog.at_level(logging.DEBUG, logger="apu"):
        machine.write_byte(address, value)
    offset = address - 0x4000
    assert writes == [(offset, value)]
    assert caplog.records[-1].getMessage() == f"Ignored APU write at register offset 0x{offset:02X}: 0x{value:02X}"

    # The new write does not make either the CPU or the APU read path available.
    with pytest.raises(NotImplementedError, match=f"CPU read at address 0x{address:04X}"):
        machine.read_byte(address)
    with pytest.raises(NotImplementedError, match=f"APU read at register offset 0x{offset:02X}"):
        machine.apu.read_byte(offset)


@pytest.mark.parametrize("address", [0x4000, 0x4004, 0x4008, 0x400C])
def test_cpu_continues_after_pulse_control_write(make_cpu, address):
    # LDA #$FF; STA channel control; NOP exercises each stub through CPU and Machine.
    _, machine = make_cpu()
    machine.write_byte(0x0000, 0xA9)
    machine.write_byte(0x0001, 0xFF)
    machine.write_byte(0x0002, 0x8D)
    machine.write_byte(0x0003, address & 0xFF)
    machine.write_byte(0x0004, 0x40)
    machine.write_byte(0x0005, 0xEA)
    emulator = Emulator(machine)

    # Execution continues with just the normal instruction cost.
    emulator.step()
    emulator.step()
    emulator.step()
    assert emulator.cpu.pc == 0x0006
    assert emulator.cpu.cycles == 8
