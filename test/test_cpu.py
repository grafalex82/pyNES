"""Verify CPU startup, repeated reset, instruction execution, and register state."""

import pytest

from cpu import CPU


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


def test_step_preserves_state_when_opcode_read_fails(make_cpu):
    # The unconnected PPU register cannot supply an opcode; retain distinctive CPU and RAM contents.
    cpu, machine = make_cpu()
    cpu.a = 0x12
    cpu.x = 0x34
    cpu.y = 0x56
    cpu.sp = 0x9A
    cpu.p = 0xE1
    cpu.pc = 0x2002
    machine.write_byte(0x0100, 0xAB)
    ram = bytes(machine.read_byte(address) for address in range(2048))

    # The read failure propagates from Machine without changing CPU state or RAM.
    with pytest.raises(NotImplementedError, match="CPU read at address 0x2002"):
        cpu.step()
    assert cpu.a == 0x12
    assert cpu.x == 0x34
    assert cpu.y == 0x56
    assert cpu.sp == 0x9A
    assert cpu.p == 0xE1
    assert cpu.pc == 0x2002
    assert bytes(machine.read_byte(address) for address in range(2048)) == ram


@pytest.mark.parametrize("initial_i", [False, True])
def test_step_sei_sets_interrupt_disable(make_cpu, initial_i):
    # Place SEI at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x78)
    cpu.interrupt_disable = initial_i

    # SEI sets I from either initial value.
    cpu.step()
    assert cpu.interrupt_disable is True
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_i", [False, True])
def test_step_cli_clears_interrupt_disable(make_cpu, initial_i):
    # Place CLI at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x58)
    cpu.interrupt_disable = initial_i

    # CLI clears I from either initial value.
    cpu.step()
    assert cpu.interrupt_disable is False
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_c", [False, True])
def test_step_clc_clears_carry(make_cpu, initial_c):
    # Place CLC at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x18)
    cpu.carry = initial_c

    # CLC clears C from either initial value.
    cpu.step()
    assert cpu.carry is False
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_c", [False, True])
def test_step_sec_sets_carry(make_cpu, initial_c):
    # Place SEC at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x38)
    cpu.carry = initial_c

    # SEC sets C from either initial value.
    cpu.step()
    assert cpu.carry is True
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_d", [False, True])
def test_step_cld_clears_decimal_flag(make_cpu, initial_d):
    # Place CLD at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xD8)
    cpu.decimal = initial_d

    # CLD clears D from either initial value.
    cpu.step()
    assert cpu.decimal is False
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_d", [False, True])
def test_step_sed_sets_decimal_flag(make_cpu, initial_d):
    # Place SED at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xF8)
    cpu.decimal = initial_d

    # SED sets D from either initial value.
    cpu.step()
    assert cpu.decimal is True
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_v", [False, True])
def test_step_clv_clears_overflow(make_cpu, initial_v):
    # Place CLV at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xB8)
    cpu.overflow = initial_v

    # CLV clears V from either initial value.
    cpu.step()
    assert cpu.overflow is False
    assert cpu.cycles == 2


def test_step_nop_advances_pc(make_cpu):
    # Place the official one-byte NOP at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xEA)

    # The opcode fetch advances PC by one byte.
    cpu.step()
    assert cpu.pc == 0x0001
    assert cpu.cycles == 2


@pytest.mark.parametrize("opcode, register", [(0xA9, "a"), (0xA2, "x"), (0xA0, "y")])
@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
def test_immediate_loads_update_register_and_nz(make_cpu, opcode, register, value):
    # Start the destination at a value different from every tested operand.
    cpu, machine = make_cpu(start_address=0x0234)
    setattr(cpu, register, 0x55)
    machine.write_byte(0x0234, opcode)
    machine.write_byte(0x0235, value)

    # Check the destination, flags, PC, and completed-instruction cycles.
    cpu.step()
    assert getattr(cpu, register) == value
    assert cpu.negative is bool(value & 0x80)
    assert cpu.zero is (value == 0)
    assert cpu.pc == 0x0236
    assert cpu.cycles == 2


@pytest.mark.parametrize("opcode, register", [(0xAD, "a"), (0xAE, "x"), (0xAC, "y")])
@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
def test_absolute_loads_update_register_and_nz(make_cpu, opcode, register, value):
    # Use distinct address bytes to test little-endian addressing.
    cpu, machine = make_cpu()
    machine.write_byte(0x0456, value)
    cpu.pc = 0x0200
    setattr(cpu, register, 0x55)
    cpu.negative = not bool(value & 0x80)
    cpu.zero = value != 0
    machine.write_byte(0x0200, opcode)
    machine.write_byte(0x0201, 0x56)
    machine.write_byte(0x0202, 0x04)

    # The selected register and N/Z reflect the fetched byte.
    cpu.step()
    assert getattr(cpu, register) == value
    assert cpu.negative is bool(value & 0x80)
    assert cpu.zero is (value == 0)
    assert cpu.pc == 0x0203
    assert cpu.cycles == 4


@pytest.mark.parametrize("opcode, register", [(0x8D, "a"), (0x8E, "x"), (0x8C, "y")])
@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
@pytest.mark.parametrize("flag", [False, True])
def test_absolute_stores_write_register_without_changing_flags(make_cpu, opcode, register, value, flag):
    # The distinct operand bytes identify whether the CPU reads the address low byte first.
    cpu, machine = make_cpu(start_address=0x0200)
    setattr(cpu, register, value)
    cpu.negative = flag
    cpu.overflow = flag
    cpu.break_flag = flag
    cpu.decimal = flag
    cpu.interrupt_disable = flag
    cpu.zero = flag
    cpu.carry = flag
    machine.write_byte(0x0200, opcode)
    machine.write_byte(0x0201, 0x56)
    machine.write_byte(0x0202, 0x04)

    # The write reaches the selected address without affecting the status flags.
    cpu.step()
    assert machine.read_byte(0x0456) == value
    assert cpu.negative is flag
    assert cpu.overflow is flag
    assert cpu.break_flag is flag
    assert cpu.decimal is flag
    assert cpu.interrupt_disable is flag
    assert cpu.zero is flag
    assert cpu.carry is flag
    assert cpu.pc == 0x0203
    assert cpu.cycles == 4


@pytest.mark.parametrize("opcode, register", [(0x8D, "a"), (0x8E, "x"), (0x8C, "y")])
@pytest.mark.parametrize(
    "high_byte, error, message",
    [
        (0x20, NotImplementedError, "CPU write at address 0x2000"),
        (0x80, PermissionError, "ROM at offset 0x0000"),
    ],
)
def test_absolute_store_propagates_write_error(make_cpu, opcode, register, high_byte, error, message):
    # Target either the unconnected PPU area or the beginning of PRG ROM.
    cpu, machine = make_cpu(start_address=0x0200)
    setattr(cpu, register, 0xA5)
    machine.write_byte(0x0200, opcode)
    machine.write_byte(0x0201, 0x00)
    machine.write_byte(0x0202, high_byte)

    # The device's diagnostic propagates before completed-instruction cycles accrue.
    with pytest.raises(error, match=message):
        cpu.step()
    assert cpu.pc == 0x0203
    assert cpu.cycles == 0


@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
def test_tsx_transfers_stack_pointer_and_updates_nz(make_cpu, value):
    # Begin with opposite flag values so TSX must update both flags.
    cpu, machine = make_cpu()
    cpu.sp = value
    cpu.x = 0x55
    cpu.negative = not bool(value & 0x80)
    cpu.zero = value != 0
    machine.write_byte(0x0000, 0xBA)

    # TSX copies SP to X and sets N and Z from the copied value.
    cpu.step()
    assert cpu.x == value
    assert cpu.negative is bool(value & 0x80)
    assert cpu.zero is (value == 0)
    assert cpu.pc == 0x0001
    assert cpu.cycles == 2


@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
@pytest.mark.parametrize("flag", [False, True])
def test_txs_transfers_x_without_changing_flags(make_cpu, value, flag):
    # Both initial flag states reveal any unintended status changes.
    cpu, machine = make_cpu()
    cpu.x = value
    cpu.sp = 0x55
    cpu.negative = flag
    cpu.overflow = flag
    cpu.break_flag = flag
    cpu.decimal = flag
    cpu.interrupt_disable = flag
    cpu.zero = flag
    cpu.carry = flag
    machine.write_byte(0x0000, 0x9A)

    # Unlike TSX, TXS does not update flags from the transferred value.
    cpu.step()
    assert cpu.sp == value
    assert cpu.negative is flag
    assert cpu.overflow is flag
    assert cpu.break_flag is flag
    assert cpu.decimal is flag
    assert cpu.interrupt_disable is flag
    assert cpu.zero is flag
    assert cpu.carry is flag
    assert cpu.pc == 0x0001
    assert cpu.cycles == 2


@pytest.mark.parametrize(
    "opcode, source, destination",
    [(0x8A, "x", "a"), (0x98, "y", "a"), (0xAA, "a", "x"), (0xA8, "a", "y")],
)
@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
def test_register_transfer_updates_destination_and_nz(make_cpu, opcode, source, destination, value):
    # Start with a distinct destination and opposite flags to reveal missed updates.
    cpu, machine = make_cpu()
    setattr(cpu, source, value)
    setattr(cpu, destination, 0x55)
    cpu.negative = not bool(value & 0x80)
    cpu.zero = value != 0
    machine.write_byte(0x0000, opcode)

    # The destination and N/Z reflect the transferred byte.
    cpu.step()
    assert getattr(cpu, destination) == value
    assert cpu.negative is bool(value & 0x80)
    assert cpu.zero is (value == 0)
    assert cpu.pc == 0x0001
    assert cpu.cycles == 2


@pytest.mark.parametrize(
    "opcode, register, initial, expected",
    [
        # INX
        (0xE8, "x", 0x00, 0x01),
        (0xE8, "x", 0x7F, 0x80),
        (0xE8, "x", 0xFF, 0x00),
        # INY
        (0xC8, "y", 0x00, 0x01),
        (0xC8, "y", 0x7F, 0x80),
        (0xC8, "y", 0xFF, 0x00),
        # DEX
        (0xCA, "x", 0x00, 0xFF),
        (0xCA, "x", 0x01, 0x00),
        (0xCA, "x", 0x80, 0x7F),
        # DEY
        (0x88, "y", 0x00, 0xFF),
        (0x88, "y", 0x01, 0x00),
        (0x88, "y", 0x80, 0x7F),
    ],
)
def test_index_increment_and_decrement(make_cpu, opcode, register, initial, expected):
    # Opposite initial flags show that the instruction updates both N and Z.
    cpu, machine = make_cpu()
    setattr(cpu, register, initial)
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0000, opcode)

    # Check the index result, its flags, and the instruction cost.
    cpu.step()
    assert getattr(cpu, register) == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0001
    assert cpu.cycles == 2


@pytest.mark.parametrize(
    "opcode, flag, taken_flag",
    [
        (0xF0, "zero", True),
        (0xD0, "zero", False),
        (0x10, "negative", False),
        (0x30, "negative", True),
        (0x90, "carry", False),
        (0xB0, "carry", True),
        (0x50, "overflow", False),
        (0x70, "overflow", True),
    ],
)
@pytest.mark.parametrize(
    "start, operand, taken, expected_pc, expected_cycles",
    [
        (0x0210, 0x00, True, 0x0212, 3),
        (0x0210, 0x05, True, 0x0217, 3),
        (0x0210, 0xFB, True, 0x020D, 3),
        (0x0270, 0x7F, True, 0x02F1, 3),
        (0x0290, 0x80, True, 0x0212, 3),
        (0x02FD, 0x01, True, 0x0300, 4),
        (0x0300, 0xFC, True, 0x02FE, 4),
        (0x02F0, 0x7F, False, 0x02F2, 2),
    ],
)
def test_conditional_branch(make_cpu, opcode, flag, taken_flag, start, operand, taken, expected_pc, expected_cycles):
    # A program in RAM selects each condition and signed displacement independently.
    cpu, machine = make_cpu()
    cpu.pc = start
    setattr(cpu, flag, taken_flag if taken else not taken_flag)
    machine.write_byte(start, opcode)
    machine.write_byte(start + 1, operand)

    # PC and cycles reflect whether the branch was taken and crossed a page.
    cpu.step()
    assert cpu.pc == expected_pc
    assert cpu.cycles == expected_cycles


def test_cycles_accumulate_across_mixed_instructions(make_cpu):
    # Execute each supported encoding once in a synthetic RAM program.
    cpu, machine = make_cpu()
    program = (0x18, 0x38, 0x58, 0x78, 0xD8, 0xF8, 0xB8, 0xEA)
    for address, opcode in enumerate(program):
        machine.write_byte(address, opcode)

    # Each step contributes two, yielding sixteen cycles in total.
    for expected_cycles in range(2, 17, 2):
        cpu.step()
        assert cpu.cycles == expected_cycles


def test_cycles_do_not_wrap_at_16_bits(make_cpu):
    # Reuse one RAM NOP to advance the cumulative counter past $FFFF.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xEA)
    for _ in range(32769):
        cpu.pc = 0x0000
        cpu.step()

    # The Python integer is not limited to a 16-bit CPU register width.
    assert cpu.cycles == 65538


def test_cycles_are_read_only_and_preserved_by_reset(make_cpu):
    # A new CPU starts at zero and counts a completed instruction.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xEA)
    assert cpu.cycles == 0
    cpu.step()
    assert cpu.cycles == 2

    # Reset does not charge instruction cycles, and callers cannot assign the counter.
    cpu.reset()
    cpu.reset()
    assert cpu.cycles == 2
    with pytest.raises(AttributeError):
        cpu.cycles = 0
    assert cpu.cycles == 2


@pytest.mark.parametrize("failed_pc", [0x0001, 0x2002])
def test_failed_step_preserves_accumulated_cycles(make_cpu, failed_pc):
    # A completed NOP precedes either an unsupported opcode or an unconnected read.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xEA)
    machine.write_byte(0x0001, 0x02)
    cpu.step()
    cpu.pc = failed_pc

    # Neither failure adds cycles or removes the completed instruction's contribution.
    with pytest.raises(NotImplementedError):
        cpu.step()
    assert cpu.cycles == 2


def test_instruction_table_has_one_entry_per_opcode():
    assert len(CPU._instruction_handlers) == 256


@pytest.mark.parametrize("opcode", [0x1A, 0x02, 0xFF])
def test_step_reports_empty_instruction_table_entry(make_cpu, opcode):
    # Pick a nonzero PC and known register values to verify state at the failed instruction.
    cpu, machine = make_cpu(start_address=0x0234)
    cpu.a = 0x12
    cpu.x = 0x34
    cpu.y = 0x56
    cpu.sp = 0x9A
    cpu.p = 0xE1
    machine.write_byte(0x0234, opcode)
    machine.write_byte(0x0100, 0xAB)
    ram = bytes(machine.read_byte(address) for address in range(2048))

    # A missing handler must report both the byte and its address without consuming it.
    with pytest.raises(NotImplementedError) as error:
        cpu.step()
    assert str(error.value) == f"CPU opcode 0x{opcode:02X} at address 0x0234 is not implemented"
    assert cpu.a == 0x12
    assert cpu.x == 0x34
    assert cpu.y == 0x56
    assert cpu.sp == 0x9A
    assert cpu.p == 0xE1
    assert cpu.pc == 0x0234
    assert bytes(machine.read_byte(address) for address in range(2048)) == ram


def test_step_retains_completed_instructions_before_unsupported_opcode(make_cpu):
    # SEI and CLD change distinct flags before the unsupported opcode.
    cpu, machine = make_cpu(start_address=0x0234)
    cpu.a = 0x12
    cpu.x = 0x34
    cpu.y = 0x56
    cpu.sp = 0x9A
    cpu.p = 0xF9
    program = (0x78, 0xD8, 0x02, 0x42)
    for offset, value in enumerate(program):
        machine.write_byte(0x0234 + offset, value)
    ram = bytes(machine.read_byte(address) for address in range(2048))

    # The failed step retains the two completed flag changes and the original program bytes.
    cpu.step()
    cpu.step()
    with pytest.raises(NotImplementedError, match="CPU opcode 0x02 at address 0x0236"):
        cpu.step()
    assert cpu.a == 0x12
    assert cpu.x == 0x34
    assert cpu.y == 0x56
    assert cpu.sp == 0x9A
    assert cpu.p == 0xF5
    assert cpu.pc == 0x0236
    assert bytes(machine.read_byte(address) for address in range(2048)) == ram


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
