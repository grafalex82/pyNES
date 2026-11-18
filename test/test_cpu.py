"""Verify CPU startup, register ranges, and conversion between status and seven boolean fields."""

import pytest

from cpu import CPU
from machine import Machine
from nesfile import NESFile


PRG_ROM_BANK_SIZE = 16384


def make_ines_header(*, prg_rom_banks, chr_rom_banks=0, mapper=0):
    """Build an ordinary iNES header with horizontal mirroring and no trainer or battery."""
    # Bytes 4/5 count PRG/CHR banks; bytes 6/7 hold the low/high mapper nibbles.
    header = bytearray(16)
    header[:4] = b"NES\x1a"
    header[4] = prg_rom_banks
    header[5] = chr_rom_banks
    header[6] = (mapper & 0x0F) << 4
    header[7] = mapper & 0xF0
    return bytes(header)


@pytest.fixture
def make_cpu(tmp_path):
    # Tests can select a PRG layout and RAM entry point without replacing memory operations.
    def create_cpu(*, prg_size=PRG_ROM_BANK_SIZE, start_address=0x0000):
        # The reset vector occupies the fourth and third bytes before the end of either PRG layout.
        prg = bytearray(prg_size)
        prg[-4:-2] = start_address.to_bytes(2, "little")
        header = make_ines_header(prg_rom_banks=prg_size // PRG_ROM_BANK_SIZE, chr_rom_banks=0, mapper=0)
        filename = tmp_path / "cpu.nes"
        filename.write_bytes(header + prg)
        machine = Machine(NESFile(filename))
        return CPU(machine), machine

    # Both components remain available for test-specific registers, data, and future instruction bytes in RAM.
    return create_cpu


@pytest.fixture
def prg_size():
    return PRG_ROM_BANK_SIZE


@pytest.fixture
def start_address():
    return 0x0000


@pytest.fixture
def cpu(make_cpu, prg_size, start_address):
    cpu, _ = make_cpu(prg_size=prg_size, start_address=start_address)
    return cpu


@pytest.mark.parametrize("prg_size, start_address", [(16384, 0x0234), (32768, 0x0678)])
def test_initializes_cpu_through_machine_reset_vector(cpu, start_address):
    # One reset after constructor clearing establishes the selected initial register profile.
    assert cpu.a == 0x00
    assert cpu.x == 0x00
    assert cpu.y == 0x00
    assert cpu.sp == 0xFD
    assert cpu.pc == start_address
    assert cpu.p == 0x24
    assert cpu.negative is False
    assert cpu.overflow is False
    assert cpu.break_flag is False
    assert cpu.decimal is False
    assert cpu.interrupt_disable is True
    assert cpu.zero is False
    assert cpu.carry is False


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
def test_p_packs_flags(cpu, flags, expected):
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
def test_p_unpacks_flags(cpu, value, expected):
    cpu.p = 0xFF
    cpu.p = value
    flags = (cpu.negative, cpu.overflow, cpu.break_flag, cpu.decimal, cpu.interrupt_disable, cpu.zero, cpu.carry)
    assert flags == expected


@pytest.mark.parametrize(
    "register, maximum", [("a", 0xFF), ("x", 0xFF), ("y", 0xFF), ("sp", 0xFF), ("p", 0xFF), ("pc", 0xFFFF)]
)
def test_register_setters_assert_value_ranges(cpu, register, maximum):
    # Both endpoints are valid; reading P always includes its constant bit 5.
    for value in (0, maximum):
        setattr(cpu, register, value)
        assert getattr(cpu, register) == (value | 0x20 if register == "p" else value)

    # Rejected values on either side must preserve the previous register or status fields.
    previous = getattr(cpu, register)
    for value in (-1, maximum + 1):
        with pytest.raises(AssertionError):
            setattr(cpu, register, value)
        assert getattr(cpu, register) == previous
