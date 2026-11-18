"""Verify conversion between the status byte and its seven boolean fields."""

import pytest

from cpu import CPU


@pytest.mark.parametrize(
    "flags, expected",
    [
        ((False, False, False, False, False, False, False), 0x20),
        ((False, False, False, False, False, False, True), 0x21),
        ((False, False, False, False, False, True, False), 0x22),
        ((False, False, False, False, True, False, False), 0x24),
        ((False, False, False, True, False, False, False), 0x28),
        ((False, False, True, False, False, False, False), 0x30),
        ((False, True, False, False, False, False, False), 0x60),
        ((True, False, False, False, False, False, False), 0xA0),
        ((True, True, True, True, True, True, True), 0xFF),
    ],
)
def test_p_packs_flags(flags, expected):
    cpu = CPU(None)
    cpu.negative, cpu.overflow, cpu.break_flag, cpu.decimal, cpu.interrupt_disable, cpu.zero, cpu.carry = flags
    assert cpu.p == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0x00, (False, False, False, False, False, False, False)),
        (0x01, (False, False, False, False, False, False, True)),
        (0x02, (False, False, False, False, False, True, False)),
        (0x04, (False, False, False, False, True, False, False)),
        (0x08, (False, False, False, True, False, False, False)),
        (0x10, (False, False, True, False, False, False, False)),
        (0x20, (False, False, False, False, False, False, False)),
        (0x40, (False, True, False, False, False, False, False)),
        (0x80, (True, False, False, False, False, False, False)),
        (0xFF, (True, True, True, True, True, True, True)),
    ],
)
def test_p_unpacks_flags(value, expected):
    cpu = CPU(None)
    cpu.p = 0xFF
    cpu.p = value
    flags = (cpu.negative, cpu.overflow, cpu.break_flag, cpu.decimal, cpu.interrupt_disable, cpu.zero, cpu.carry)
    assert flags == expected


@pytest.mark.parametrize(
    "register, maximum", [("a", 0xFF), ("x", 0xFF), ("y", 0xFF), ("sp", 0xFF), ("p", 0xFF), ("pc", 0xFFFF)]
)
def test_register_setters_assert_value_ranges(register, maximum):
    # Both endpoints are valid; reading P always includes its constant bit 5.
    cpu = CPU(None)
    for value in (0, maximum):
        setattr(cpu, register, value)
        assert getattr(cpu, register) == (value | 0x20 if register == "p" else value)

    # Rejected values on either side must preserve the previous register or status fields.
    previous = getattr(cpu, register)
    for value in (-1, maximum + 1):
        with pytest.raises(AssertionError):
            setattr(cpu, register, value)
        assert getattr(cpu, register) == previous
