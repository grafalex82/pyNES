"""Verify CPU reset and trace formatting independently of instruction execution."""

import logging

import pytest


@pytest.mark.parametrize("prg_size, start_address", [(16384, 0x0234), (32768, 0xABCD)])
def test_logs_completed_startup_reset(make_cpu, caplog, prg_size, start_address):
    # Capture construction itself so a duplicate startup event cannot go unnoticed.
    with caplog.at_level(logging.DEBUG, logger="cpu"):
        make_cpu(prg_size=prg_size, start_address=start_address)

    # Compare the full message, including register order, separators, and flag formatting.
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.name == "cpu"
    assert record.levelno == logging.DEBUG
    assert record.getMessage() == f"Reset completed: A=00 X=00 Y=00 SP=FD PC={start_address:04X} P=--1--I-- CYC=0"


@pytest.mark.parametrize("prg_size, start_address", [(16384, 0x0234), (32768, 0x2002)])
@pytest.mark.parametrize("initial_p, expected_p", [(0x00, "--1--I--"), (0xDB, "NV1BDIZC")])
def test_logs_completed_repeated_reset(cpu, caplog, start_address, initial_p, expected_p):
    # Nonzero registers, wrapping SP, and clear I distinguish the result from the pre-reset state.
    cpu.a = 0x12
    cpu.x = 0x34
    cpu.y = 0x56
    cpu.sp = 0x01
    cpu.p = initial_p

    # Each call must report one fresh snapshot after SP, I, and PC have changed.
    with caplog.at_level(logging.DEBUG, logger="cpu"):
        for expected_sp in ("FE", "FB"):
            caplog.clear()
            cpu.pc = 0xABCD
            cpu.interrupt_disable = False
            cpu.reset()
            assert len(caplog.records) == 1
            record = caplog.records[0]
            assert record.name == "cpu"
            assert record.levelno == logging.DEBUG
            expected = f"Reset completed: A=12 X=34 Y=56 SP={expected_sp} PC={start_address:04X} P={expected_p} CYC=0"
            assert record.getMessage() == expected


@pytest.mark.parametrize(
    "value, expected_flags",
    [
        (0x00, "--1-----"),
        (0x01, "--1----C"),
        (0x02, "--1---Z-"),
        (0x04, "--1--I--"),
        (0x08, "--1-D---"),
        (0x10, "--1B----"),
        (0x40, "-V1-----"),
        (0x80, "N-1-----"),
        (0x05, "--1--I-C"),
        (0xFF, "NV1BDIZC"),
    ],
)
def test_log_state_reports_current_registers_and_flags(cpu, caplog, value, expected_flags):
    # Calling the helper directly must preserve the caller's registers and flags, including clear I.
    cpu.a = 0x12
    cpu.x = 0x34
    cpu.y = 0x56
    cpu.sp = 0x9A
    cpu.pc = 0xBCDE
    cpu.p = value

    # Percent signs in event text remain literal; only the logger's own format supplies register fields.
    with caplog.at_level(logging.DEBUG, logger="cpu"):
        cpu.log_state("Checkpoint 50%")

    # Check one current-state snapshot, including the fixed bit 5 and every mutable flag position.
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.name == "cpu"
    assert record.levelno == logging.DEBUG
    assert record.getMessage() == f"Checkpoint 50%: A=12 X=34 Y=56 SP=9A PC=BCDE P={expected_flags} CYC=0"
    assert (cpu.a, cpu.x, cpu.y, cpu.sp, cpu.pc, cpu.p) == (0x12, 0x34, 0x56, 0x9A, 0xBCDE, value | 0x20)


@pytest.mark.parametrize(
    "address, instruction_bytes, mnemonic, operands, prefix",
    [
        (0x8000, (0x78,), "SEI", "", "8000   78         SEI                     "),
        (0x8001, (0xA9, 0x10), "LDA", "#$10", "8001   A9 10      LDA #$10                "),
        (0x8003, (0x4C, 0x00, 0xC0), "JMP", "$C000", "8003   4C 00 C0   JMP $C000               "),
    ],
)
def test_log_instruction_formats_supplied_metadata_without_accessing_memory(
    make_cpu, caplog, monkeypatch, address, instruction_bytes, mnemonic, operands, prefix
):
    # Known state and a sentinel byte make accidental mutation visible.
    cpu, machine = make_cpu()
    cpu.a, cpu.x, cpu.y, cpu.sp, cpu.pc, cpu.p = 0x12, 0x34, 0x56, 0x9A, 0xBCDE, 0x85
    cpu._cycles = 1234
    machine.write_byte(0x0100, 0xAB)

    # Neither helper may access memory; formatting uses only the supplied instruction metadata.
    with monkeypatch.context() as blocked, caplog.at_level(logging.DEBUG, logger="cpu"):
        blocked.setattr(machine, "read_byte", lambda address: pytest.fail("Unexpected memory read"))
        blocked.setattr(machine, "write_byte", lambda address, value: pytest.fail("Unexpected memory write"))
        cpu.log_instruction(address, instruction_bytes, mnemonic, operands)

    # Compare the complete line and verify the observed state and memory are unchanged.
    assert len(caplog.records) == 1
    assert caplog.records[0].getMessage() == prefix + " A=12 X=34 Y=56 SP=9A PC=BCDE P=N-1--I-C CYC=1234"
    assert (cpu.a, cpu.x, cpu.y, cpu.sp, cpu.pc, cpu.p, cpu.cycles) == (0x12, 0x34, 0x56, 0x9A, 0xBCDE, 0xA5, 1234)
    assert machine.read_byte(0x0100) == 0xAB


def test_log_instruction_skips_formatting_when_debug_is_disabled(cpu, caplog):
    # Iterating this input would reveal any attempted instruction-byte formatting.
    instruction_bytes = (pytest.fail("Unexpected trace formatting") for _ in range(1))

    # INFO disables the CPU's DEBUG trace before the helper touches its inputs.
    with caplog.at_level(logging.INFO, logger="cpu"):
        cpu.log_instruction(0x8000, instruction_bytes, "SEI")
    assert not caplog.records


