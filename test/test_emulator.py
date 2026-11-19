"""Verify the shared execution controls using synthetic cartridges."""

import pytest

from conftest import make_ines_header
from emulator import Emulator
from machine import Machine
from nesfile import NESFile


@pytest.fixture
def make_machine(tmp_path):
    def create_machine(start_address=0x0000):
        # Install the reset vector in a synthetic 16 KiB cartridge.
        prg = bytearray(16384)
        prg[-4:-2] = start_address.to_bytes(2, "little")
        path = tmp_path / "emulator.nes"
        path.write_bytes(make_ines_header(prg_rom_banks=1) + prg)
        return Machine(NESFile(path))

    return create_machine


def test_construction_starts_cpu_once_without_executing_or_clearing_ram(make_machine):
    # SEI followed by an unsupported opcode reveals any execution during construction.
    machine = make_machine(start_address=0x0200)
    machine.write_byte(0x0200, 0x78)
    machine.write_byte(0x0201, 0x02)
    machine.write_byte(0x0100, 0xA5)
    emulator = Emulator(machine)

    # One startup reset leaves SP at $FD and the entry instruction untouched.
    assert emulator.cpu.a == 0
    assert emulator.cpu.x == 0
    assert emulator.cpu.y == 0
    assert emulator.cpu.sp == 0xFD
    assert emulator.cpu.pc == 0x0200
    assert emulator.cpu.p == 0x24
    assert emulator.cpu.cycles == 0
    assert machine.read_byte(0x0200) == 0x78
    assert machine.read_byte(0x0100) == 0xA5


def test_step_executes_exactly_one_instruction(make_machine):
    # The following unsupported opcode would fail if step fetched more than once.
    machine = make_machine()
    machine.write_byte(0, 0x78)
    machine.write_byte(1, 0x02)
    emulator = Emulator(machine)
    emulator.cpu.interrupt_disable = False

    # The facade exposes the same CPU after its one instruction.
    cpu = emulator.cpu
    assert emulator.step() is None
    assert emulator.cpu is cpu
    assert cpu.pc == 1
    assert cpu.cycles == 2
    assert cpu.interrupt_disable is True


def test_separate_emulators_have_independent_cpu_state(make_machine):
    first_machine = make_machine()
    second_machine = make_machine()
    first_machine.write_byte(0, 0x38)
    second_machine.write_byte(0, 0xEA)
    first = Emulator(first_machine)
    second = Emulator(second_machine)

    first.step()
    assert first.cpu is not second.cpu
    assert first.cpu.pc == 1
    assert first.cpu.cycles == 2
    assert first.cpu.carry is True
    assert second.cpu.pc == 0
    assert second.cpu.cycles == 0
    assert second.cpu.carry is False


@pytest.mark.parametrize("budget, expected_steps", [(0, 0), (1, 1), (2, 1), (3, 2), (6, 3)])
def test_run_stops_at_first_complete_instruction_boundary(make_machine, budget, expected_steps):
    # SEC, CLC, NOP and SEI expose both the instruction boundary and the flag effects.
    machine = make_machine()
    for address, opcode in enumerate((0x38, 0x18, 0xEA, 0x78)):
        machine.write_byte(address, opcode)
    emulator = Emulator(machine)
    emulator.cpu.interrupt_disable = False

    # No instruction beyond the budget boundary may execute.
    assert emulator.run(budget) is None
    assert emulator.cpu.pc == expected_steps
    assert emulator.cpu.cycles == 2 * expected_steps
    assert emulator.cpu.carry is (expected_steps == 1)
    assert emulator.cpu.interrupt_disable is False
    assert [machine.read_byte(address) for address in range(4)] == [0x38, 0x18, 0xEA, 0x78]


def test_run_zero_does_not_fetch_from_unconnected_memory(make_machine):
    emulator = Emulator(make_machine(start_address=0x4000))
    assert emulator.run(0) is None
    assert emulator.cpu.pc == 0x4000
    assert emulator.cpu.sp == 0xFD
    assert emulator.cpu.p == 0x24
    assert emulator.cpu.cycles == 0


def test_run_uses_fresh_budgets_after_prior_execution_and_overshoot(make_machine):
    machine = make_machine()
    for address in range(9):
        machine.write_byte(address, 0xEA)
    emulator = Emulator(machine)

    # An existing total must not be mistaken for the new target.
    emulator.run(10)
    emulator.run(4)
    assert emulator.cpu.pc == 7
    assert emulator.cpu.cycles == 14

    # Consecutive odd budgets each retain their own overshoot.
    emulator.cpu.pc = 0
    emulator.run(3)
    assert emulator.cpu.pc == 2
    assert emulator.cpu.cycles == 18
    emulator.run(3)
    assert emulator.cpu.pc == 4
    assert emulator.cpu.cycles == 22


def test_run_propagates_failure_after_retaining_completed_instruction(make_machine):
    machine = make_machine()
    machine.write_byte(0, 0x78)
    machine.write_byte(1, 0x02)
    emulator = Emulator(machine)
    emulator.cpu.interrupt_disable = False

    # The exact boundary returns before the unsupported byte is fetched.
    emulator.run(2)
    assert emulator.cpu.pc == 1
    assert emulator.cpu.cycles == 2
    assert emulator.cpu.interrupt_disable is True

    # A longer budget propagates the failure and leaves the completed SEI intact.
    emulator.cpu.pc = 0
    emulator.cpu.interrupt_disable = False
    with pytest.raises(NotImplementedError, match="opcode 0x02 at address 0x0001"):
        emulator.run(3)
    assert emulator.cpu.pc == 1
    assert emulator.cpu.cycles == 4
    assert emulator.cpu.interrupt_disable is True
    assert machine.read_byte(1) == 0x02


def test_reset_preserves_connected_cpu_memory_and_cycles(make_machine):
    # Keep code and stack-page data in the supplied Machine across repeated resets.
    machine = make_machine(start_address=0x0200)
    machine.write_byte(0x0200, 0xEA)
    machine.write_byte(0x0201, 0x02)
    machine.write_byte(0x0100, 0xA5)
    emulator = Emulator(machine)
    cpu = emulator.cpu
    emulator.step()
    cpu.a = 0x12
    cpu.x = 0x34
    cpu.y = 0x56
    cpu.sp = 0x01
    cpu.p = 0xDB

    # Each reset loads the vector once, wraps SP, sets I, and preserves other state.
    for expected_sp in (0xFE, 0xFB):
        cpu.pc = 0x2002
        cpu.interrupt_disable = False
        assert emulator.reset() is None
        assert emulator.cpu is cpu
        assert cpu.a == 0x12
        assert cpu.x == 0x34
        assert cpu.y == 0x56
        assert cpu.sp == expected_sp
        assert cpu.pc == 0x0200
        assert cpu.p == 0xFF
        assert cpu.cycles == 2
        assert machine.read_byte(0x0200) == 0xEA
        assert machine.read_byte(0x0201) == 0x02
        assert machine.read_byte(0x0100) == 0xA5

    # Executing the preserved RAM instruction confirms the CPU still uses the supplied Machine.
    emulator.step()
    assert cpu.pc == 0x0201
    assert cpu.cycles == 4
