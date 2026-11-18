"""Verify conversion between the status byte and its six boolean flags."""

import pytest

from cpu import CPU


@pytest.mark.parametrize(
    "flags, expected",
    [
        ((False, False, False, False, False, False), 0x20),
        ((False, False, False, False, False, True), 0x21),
        ((False, False, False, False, True, False), 0x22),
        ((False, False, False, True, False, False), 0x24),
        ((False, False, True, False, False, False), 0x28),
        ((False, True, False, False, False, False), 0x60),
        ((True, False, False, False, False, False), 0xA0),
        ((True, True, True, True, True, True), 0xEF),
    ],
)
def test_p_packs_flags(flags, expected):
    cpu = CPU(None)
    cpu.negative, cpu.overflow, cpu.decimal, cpu.interrupt_disable, cpu.zero, cpu.carry = flags
    assert cpu.p == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0x00, (False, False, False, False, False, False)),
        (0x01, (False, False, False, False, False, True)),
        (0x02, (False, False, False, False, True, False)),
        (0x04, (False, False, False, True, False, False)),
        (0x08, (False, False, True, False, False, False)),
        (0x40, (False, True, False, False, False, False)),
        (0x80, (True, False, False, False, False, False)),
        (0xFF, (True, True, True, True, True, True)),
    ],
)
def test_p_unpacks_flags(value, expected):
    cpu = CPU(None)
    cpu.p = 0xFF
    cpu.p = value
    assert (cpu.negative, cpu.overflow, cpu.decimal, cpu.interrupt_disable, cpu.zero, cpu.carry) == expected
