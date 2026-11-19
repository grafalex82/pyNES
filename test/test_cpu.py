"""Verify CPU startup, repeated reset, instruction execution, and register state."""

import logging

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
    # Tests can select the memory layout and entry point while using real memory operations.
    def create_cpu(*, prg_size=PRG_ROM_BANK_SIZE, start_address=0x0000, prg_program=b""):
        # Place PRG code at the mapped entry and install the reset vector in the last bank.
        prg = bytearray(prg_size)
        prg_offset = (start_address - 0x8000) & (prg_size - 1)
        prg[prg_offset:prg_offset + len(prg_program)] = prg_program
        prg[-4:-2] = start_address.to_bytes(2, "little")

        # Connect the cartridge before CPU construction reads its reset vector.
        header = make_ines_header(prg_rom_banks=prg_size // PRG_ROM_BANK_SIZE, chr_rom_banks=0, mapper=0)
        filename = tmp_path / "cpu.nes"
        filename.write_bytes(header + prg)
        machine = Machine(NESFile(filename))
        return CPU(machine), machine

    # Both components remain available for test-specific registers, data, and instruction bytes in RAM.
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


@pytest.mark.parametrize("prg_size, start_address", [(16384, 0x0234), (32768, 0x2002)])
@pytest.mark.parametrize("flag_value", [False, True])
@pytest.mark.parametrize(
    "initial_sp, expected_sp_values",
    [(0x00, (0xFD, 0xFA)), (0x01, (0xFE, 0xFB)), (0x03, (0x00, 0xFD)), (0xFD, (0xFA, 0xF7))],
)
def test_repeated_reset_preserves_registers_and_flags(cpu, start_address, flag_value, initial_sp, expected_sp_values):
    # Nonzero registers and both flag values distinguish reset from constructor-only initialization.
    cpu.a = 0x12
    cpu.x = 0x34
    cpu.y = 0x56
    cpu.sp = initial_sp
    cpu.negative = flag_value
    cpu.overflow = flag_value
    cpu.break_flag = flag_value
    cpu.decimal = flag_value
    cpu.zero = flag_value
    cpu.carry = flag_value

    # Each reset must restore PC and I; fetching $2002 would raise the unimplemented PPU error.
    for expected_sp in expected_sp_values:
        cpu.pc = 0xABCD
        cpu.interrupt_disable = False
        cpu.reset()
        assert cpu.a == 0x12
        assert cpu.x == 0x34
        assert cpu.y == 0x56
        assert cpu.sp == expected_sp
        assert cpu.pc == start_address
        assert cpu.p == (0xFF if flag_value else 0x24)
        assert cpu.negative is flag_value
        assert cpu.overflow is flag_value
        assert cpu.break_flag is flag_value
        assert cpu.decimal is flag_value
        assert cpu.interrupt_disable is True
        assert cpu.zero is flag_value
        assert cpu.carry is flag_value


@pytest.mark.parametrize("prg_size", [16384, 32768])
def test_repeated_reset_preserves_ram(make_cpu, prg_size):
    # The generic factory leaves RAM empty so this test supplies its own contents.
    cpu, machine = make_cpu(prg_size=prg_size)
    ram = bytes(range(256)) * 8
    for address, value in enumerate(ram):
        machine.write_byte(address, value)

    # Wrapping SP across zero must not push data onto the stack or clear RAM.
    cpu.sp = 0x01
    cpu.reset()
    cpu.reset()
    assert bytes(machine.read_byte(address) for address in range(2048)) == ram


def test_fetch_byte_and_word_advance_pc(make_cpu):
    # Distinct bytes reveal a reversed word or an off-by-one fetch.
    cpu, machine = make_cpu(start_address=0x0234)
    machine.write_byte(0x0234, 0xA5)
    machine.write_byte(0x0235, 0x34)
    machine.write_byte(0x0236, 0x12)

    # Each fetch starts where the previous one left PC.
    assert cpu._fetch_byte() == 0xA5
    assert cpu.pc == 0x0235
    assert cpu._fetch_word() == 0x1234
    assert cpu.pc == 0x0237


def test_fetch_word_wraps_from_prg_rom_to_ram(make_cpu):
    # The last PRG byte and first RAM byte form the word across the address boundary.
    cpu, machine = make_cpu(start_address=0xFFFF, prg_program=b"\x34")
    machine.write_byte(0x0000, 0x12)

    # The high byte is read at $0000 and the next PC is $0001.
    assert cpu._fetch_word() == 0x1234
    assert cpu.pc == 0x0001


def test_fetch_word_preserves_pc_when_second_read_fails(cpu):
    # The last RAM mirror byte is mapped, but the next address is a PPU register.
    cpu.pc = 0x1FFF

    # A partial word leaves PC at the start of the fetch.
    with pytest.raises(NotImplementedError, match="CPU read at address 0x2000"):
        cpu._fetch_word()
    assert cpu.pc == 0x1FFF


def test_step_preserves_pc_when_opcode_read_fails(cpu):
    # The unconnected PPU register cannot supply an opcode.
    cpu.pc = 0x2002

    # The read failure propagates from Machine at the original PC.
    with pytest.raises(NotImplementedError, match="CPU read at address 0x2002"):
        cpu.step()
    assert cpu.pc == 0x2002


@pytest.mark.parametrize("initial_i", [False, True])
def test_step_sei_sets_interrupt_disable(make_cpu, initial_i):
    # Place SEI at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x78)
    cpu.interrupt_disable = initial_i

    # SEI sets I from either initial value.
    cpu.step()
    assert cpu.interrupt_disable is True


@pytest.mark.parametrize("initial_i", [False, True])
def test_step_cli_clears_interrupt_disable(make_cpu, initial_i):
    # Place CLI at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x58)
    cpu.interrupt_disable = initial_i

    # CLI clears I from either initial value.
    cpu.step()
    assert cpu.interrupt_disable is False


def test_instruction_table_has_one_entry_per_opcode():
    assert len(CPU._instruction_handlers) == 256


@pytest.mark.parametrize("opcode", [0x1A, 0xA9, 0xFF])
def test_step_reports_empty_instruction_table_entry(make_cpu, opcode):
    # Pick a nonzero PC and known register values to verify state at the failed instruction.
    cpu, machine = make_cpu(start_address=0x0234)
    cpu.a, cpu.x, cpu.y, cpu.sp, cpu.p = 0x12, 0x34, 0x56, 0x9A, 0xE1
    machine.write_byte(0x0234, opcode)

    # A missing handler must report both the byte and its address without consuming it.
    with pytest.raises(NotImplementedError) as error:
        cpu.step()
    assert str(error.value) == f"CPU opcode 0x{opcode:02X} at address 0x0234 is not implemented"
    assert (cpu.a, cpu.x, cpu.y, cpu.sp, cpu.p, cpu.pc) == (0x12, 0x34, 0x56, 0x9A, 0xE1, 0x0234)
    assert machine.read_byte(0x0234) == opcode


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
    assert record.getMessage() == f"Reset completed: A=00 X=00 Y=00 SP=FD PC={start_address:04X} P=--1--I--"


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
            expected = f"Reset completed: A=12 X=34 Y=56 SP={expected_sp} PC={start_address:04X} P={expected_p}"
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
    assert record.getMessage() == f"Checkpoint 50%: A=12 X=34 Y=56 SP=9A PC=BCDE P={expected_flags}"
    assert (cpu.a, cpu.x, cpu.y, cpu.sp, cpu.pc, cpu.p) == (0x12, 0x34, 0x56, 0x9A, 0xBCDE, value | 0x20)


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
