"""Verify temporary audio-channel control write stubs."""

import logging

import pytest

from emulator import Emulator


@pytest.mark.parametrize("value", [0x00, 0x7F, 0xFF])
@pytest.mark.parametrize("address", [0x4000, 0x4004, 0x4008, 0x400C])
def test_pulse_control_write_routes_to_apu_and_reads_zero(make_cpu, monkeypatch, caplog, value, address):
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

    # Reads return the deterministic approximation rather than the written byte.
    assert machine.read_byte(address) == 0
    assert machine.apu.read_byte(offset) == 0


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


def test_pulse2_timer_low_accepts_all_bytes_and_reads_zero(make_cpu, caplog):
    # Every byte reaches the silent APU, which records each ignored write in its component log.
    _, machine = make_cpu()
    with caplog.at_level(logging.DEBUG, logger="apu"):
        for value in range(256):
            machine.write_byte(0x4006, value)
    assert [record.getMessage() for record in caplog.records] == [
        f"Ignored APU write at register offset 0x06: 0x{value:02X}" for value in range(256)
    ]

    # Reads return zero even after all possible write values.
    assert machine.read_byte(0x4006) == 0
    assert machine.apu.read_byte(0x06) == 0


def test_cpu_continues_after_pulse2_timer_low_write(make_cpu):
    # The store is an ordinary four-cycle instruction and the following instruction remains executable.
    _, machine = make_cpu()
    for address, byte in enumerate((0xA9, 0xFF, 0x8D, 0x06, 0x40, 0xEA)):
        machine.write_byte(address, byte)
    emulator = Emulator(machine)
    for _ in range(3):
        emulator.step()
    assert emulator.cpu.pc == 6
    assert emulator.cpu.cycles == 8


def test_cpu_reads_new_dummy_register_after_write(make_cpu):
    # STA and LDA through Machine exercise a newly supported register and the resulting CPU flags.
    _, machine = make_cpu()
    for address, byte in enumerate((0xA9, 0xFF, 0x8D, 0x09, 0x40, 0xAD, 0x09, 0x40)):
        machine.write_byte(address, byte)
    emulator = Emulator(machine)
    for _ in range(3):
        emulator.step()
    assert emulator.cpu.a == 0
    assert emulator.cpu.zero
    assert not emulator.cpu.negative
    assert emulator.cpu.pc == 8
