"""Verify CPU reset and state logging."""

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
    assert cpu.a == 0x12
    assert cpu.x == 0x34
    assert cpu.y == 0x56
    assert cpu.sp == 0x9A
    assert cpu.pc == 0xBCDE
    assert cpu.p == value | 0x20


def test_log_instruction_skips_formatting_when_debug_is_disabled(cpu, caplog):
    # Iterating this input would reveal any attempted instruction-byte formatting.
    instruction_bytes = (pytest.fail("Unexpected trace formatting") for _ in range(1))

    # INFO disables the CPU's DEBUG trace before the helper touches its inputs.
    with caplog.at_level(logging.INFO, logger="cpu"):
        cpu.log_instruction(0x8000, instruction_bytes, "SEI")
    assert not caplog.records

