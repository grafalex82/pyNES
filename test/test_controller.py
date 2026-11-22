"""Verify standard controller serial behavior through the CPU memory map."""

import logging

import pytest

from emulator import Emulator


@pytest.mark.parametrize("button, expected", [
    ("A",      [1, 0, 0, 0, 0, 0, 0, 0]),
    ("B",      [0, 1, 0, 0, 0, 0, 0, 0]),
    ("Select", [0, 0, 1, 0, 0, 0, 0, 0]),
    ("Start",  [0, 0, 0, 1, 0, 0, 0, 0]),
    ("Up",     [0, 0, 0, 0, 1, 0, 0, 0]),
    ("Down",   [0, 0, 0, 0, 0, 1, 0, 0]),
    ("Left",   [0, 0, 0, 0, 0, 0, 1, 0]),
    ("Right",  [0, 0, 0, 0, 0, 0, 0, 1]),
])
def test_each_button_and_serial_order(make_cpu, button, expected):
    # Capture one pressed button in the controller's serial report.
    _, machine = make_cpu()
    machine.controllers[0].set_button(button, True)
    machine.write_byte(0x4016, 1)
    machine.write_byte(0x4016, 0)

    # The eight buttons appear in order; subsequent reads return one.
    assert [machine.read_byte(0x4016) for _ in range(8)] == expected
    assert machine.read_byte(0x4016) == 1
    assert machine.read_byte(0x4016) == 1


def test_independent_ports_and_latched_states(make_cpu):
    _, machine = make_cpu()
    first, second = machine.controllers
    first.set_button("A", True)
    first.set_button("Select", True)
    second.set_button("B", True)
    machine.write_byte(0x4016, 0xFF)
    machine.write_byte(0x4016, 0xFE)
    first.set_button("A", False)
    second.set_button("Right", True)
    assert [machine.read_byte(0x4016) for _ in range(3)] == [1, 0, 1]
    assert [machine.read_byte(0x4017) for _ in range(8)] == [0, 1, 0, 0, 0, 0, 0, 0]
    assert [machine.read_byte(0x4016) for _ in range(5)] == [0, 0, 0, 0, 0]
    machine.write_byte(0x4016, 1)
    machine.write_byte(0x4016, 0)
    assert [machine.read_byte(0x4016) for _ in range(8)] == [0, 0, 1, 0, 0, 0, 0, 0]
    assert [machine.read_byte(0x4017) for _ in range(8)] == [0, 1, 0, 0, 0, 0, 0, 1]


def test_high_strobe_reads_current_a_and_low_writes_do_not_relatch(make_cpu):
    _, machine = make_cpu()
    controller = machine.controllers[0]
    machine.write_byte(0x4016, 1)
    assert machine.read_byte(0x4016) == 0
    controller.set_button("A", True)
    controller.set_button("B", True)
    assert [machine.read_byte(0x4016) for _ in range(3)] == [1, 1, 1]
    machine.write_byte(0x4016, 0x80)
    assert machine.read_byte(0x4016) == 1
    controller.set_button("B", False)
    machine.write_byte(0x4016, 0xFE)
    assert machine.read_byte(0x4016) == 1
    assert machine.read_byte(0x4016) == 0


def test_button_logging_only_on_change(make_cpu, caplog):
    _, machine = make_cpu()
    with caplog.at_level(logging.DEBUG, logger="controller"):
        machine.controllers[0].set_button("A", True)
        machine.controllers[0].set_button("A", True)
        machine.controllers[0].set_button("A", False)
    assert [record.getMessage() for record in caplog.records] == [
        "Controller button A pressed", "Controller button A released"
    ]


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


