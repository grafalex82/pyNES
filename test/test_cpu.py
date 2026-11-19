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


@pytest.mark.parametrize("prg_size, start_address", [(16384, 0x0234), (32768, 0x4000)])
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

    # Each reset restores PC and I without attempting a fetch from the unconnected $4000 address.
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


@pytest.mark.parametrize("initial_sp, final_sp, high_address, low_address", [
    (0xFD, 0xFB, 0x01FD, 0x01FC),
    (0x00, 0xFE, 0x0100, 0x01FF),
])
def test_jsr_absolute_pushes_return_address(make_cpu, initial_sp, final_sp, high_address, low_address):
    # Asymmetric destination and return addresses expose reversed bytes.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.sp = initial_sp
    machine.write_byte(0x0567, 0x20)
    machine.write_byte(0x0568, 0x34)
    machine.write_byte(0x0569, 0x12)

    # The saved address is the last operand byte, with SP wrapping within the stack page.
    cpu.step()
    assert cpu.pc == 0x1234
    assert cpu.sp == final_sp
    assert machine.read_byte(high_address) == 0x05
    assert machine.read_byte(low_address) == 0x69
    assert cpu.cycles == 6


def test_jsr_absolute_fetches_high_operand_after_stack_writes(make_cpu):
    # Both operand bytes overlap the two stack destinations.
    cpu, machine = make_cpu(start_address=0x01FA)
    cpu.sp = 0xFC
    machine.write_byte(0x01FA, 0x20)
    machine.write_byte(0x01FB, 0x34)
    machine.write_byte(0x01FC, 0x99)

    # The low operand was already fetched; the high operand is replaced by the first push.
    cpu.step()
    assert cpu.pc == 0x0134
    assert cpu.sp == 0xFA
    assert machine.read_byte(0x01FC) == 0x01
    assert machine.read_byte(0x01FB) == 0xFC
    assert cpu.cycles == 6


@pytest.mark.parametrize("initial_sp, final_sp, low_address, high_address", [
    (0xFB, 0xFD, 0x01FC, 0x01FD),
    (0xFE, 0x00, 0x01FF, 0x0100),
])
def test_rts_pulls_return_address(make_cpu, initial_sp, final_sp, low_address, high_address):
    # Distinct stack bytes expose reversed pulls, including across the stack boundary.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.sp = initial_sp
    machine.write_byte(0x0567, 0x60)
    machine.write_byte(low_address, 0x34)
    machine.write_byte(high_address, 0x12)

    # Returning resumes after the stored address without consuming the stack bytes.
    cpu.step()
    assert cpu.pc == 0x1235
    assert cpu.sp == final_sp
    assert machine.read_byte(low_address) == 0x34
    assert machine.read_byte(high_address) == 0x12
    assert cpu.cycles == 6


@pytest.mark.parametrize("initial, expected, carry", [
    (0x00, 0x00, False),
    (0x01, 0x02, False),
    (0x40, 0x80, False),
    (0x80, 0x00, True),
    (0xFF, 0xFE, True),
])
@pytest.mark.parametrize("incoming_carry", [False, True])
def test_asl_accumulator(make_cpu, initial, expected, carry, incoming_carry):
    # Set the flags opposite to their expected results.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0x0A)

    # Check the shifted value and flags without relying on unrelated state.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0568
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial, expected, carry", [
    (0x00, 0x00, False),
    (0x01, 0x00, True),
    (0x02, 0x01, False),
    (0x80, 0x40, False),
    (0xFF, 0x7F, True),
])
@pytest.mark.parametrize("incoming_carry", [False, True])
def test_lsr_accumulator(make_cpu, initial, expected, carry, incoming_carry):
    # Set the flags opposite to their expected results.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0x4A)

    # Check the shifted value and flags without relying on unrelated state.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0568
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial, incoming_carry, expected, carry", [
    (0x00, False, 0x00, False),
    (0x00, True, 0x01, False),
    (0x80, False, 0x00, True),
    (0x80, True, 0x01, True),
    (0x40, False, 0x80, False),
    (0x40, True, 0x81, False),
    (0xFF, True, 0xFF, True),
])
def test_rol_accumulator(make_cpu, initial, incoming_carry, expected, carry):
    # Incoming and outgoing carry are varied independently.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0x2A)

    # The rotated byte determines the resulting flags.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0568
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial, incoming_carry, expected, carry", [
    (0x00, False, 0x00, False),
    (0x00, True, 0x80, False),
    (0x01, False, 0x00, True),
    (0x01, True, 0x80, True),
    (0x02, False, 0x01, False),
    (0x02, True, 0x81, False),
    (0xFF, True, 0xFF, True),
])
def test_ror_accumulator(make_cpu, initial, incoming_carry, expected, carry):
    # Incoming and outgoing carry are varied independently.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0x6A)

    # The rotated byte determines the resulting flags.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0568
    assert cpu.cycles == 2


def test_jmp_absolute_loads_destination(make_cpu):
    # An asymmetric target exposes reversed operand bytes.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x4C)
    machine.write_byte(0x0001, 0x34)
    machine.write_byte(0x0002, 0x12)

    # The destination becomes PC without fetching an instruction there.
    cpu.step()
    assert cpu.pc == 0x1234
    assert cpu.cycles == 3


def test_jmp_indirect_loads_destination(make_cpu):
    # Distinct pointer and target bytes expose incorrect address or byte order.
    cpu, machine = make_cpu(start_address=0x0200)
    machine.write_byte(0x0200, 0x6C)
    machine.write_byte(0x0201, 0x34)
    machine.write_byte(0x0202, 0x12)
    machine.write_byte(0x1234, 0x78)
    machine.write_byte(0x1235, 0x56)

    # The target is read from the two consecutive pointer locations.
    cpu.step()
    assert cpu.pc == 0x5678
    assert cpu.cycles == 5


def test_jmp_indirect_wraps_pointer_within_page(make_cpu):
    # A different value on the next page distinguishes the original CPU's behavior.
    cpu, machine = make_cpu(start_address=0x0400)
    machine.write_byte(0x0400, 0x6C)
    machine.write_byte(0x0401, 0xFF)
    machine.write_byte(0x0402, 0x12)
    machine.write_byte(0x12FF, 0x78)
    machine.write_byte(0x1200, 0x56)
    machine.write_byte(0x1300, 0x9A)

    # The high target byte comes from the start of the same page.
    cpu.step()
    assert cpu.pc == 0x5678
    assert cpu.cycles == 5


def test_jmp_indirect_wraps_pointer_at_end_of_address_space(make_cpu):
    # ROM supplies the low target byte at $FFFF and a zero high byte at $FF00.
    cpu, machine = make_cpu(start_address=0xFFFF, prg_program=b"\x78")
    cpu.pc = 0x0200
    machine.write_byte(0x0200, 0x6C)
    machine.write_byte(0x0201, 0xFF)
    machine.write_byte(0x0202, 0xFF)
    machine.write_byte(0x0000, 0x56)

    # The high byte comes from $FF00, not $0000.
    cpu.step()
    assert cpu.pc == 0x0078
    assert cpu.cycles == 5


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
    with pytest.raises(NotImplementedError, match="PPU read at register offset 0x00"):
        cpu._fetch_word()
    assert cpu.pc == 0x1FFF


def test_step_preserves_state_when_opcode_read_fails(make_cpu):
    # The unconnected address cannot supply an opcode; retain distinctive CPU and RAM contents.
    cpu, machine = make_cpu()
    cpu.a = 0x12
    cpu.x = 0x34
    cpu.y = 0x56
    cpu.sp = 0x9A
    cpu.p = 0xE1
    cpu.pc = 0x4000
    machine.write_byte(0x0100, 0xAB)
    ram = bytes(machine.read_byte(address) for address in range(2048))

    # The read failure propagates from Machine without changing CPU state or RAM.
    with pytest.raises(NotImplementedError, match="CPU read at address 0x4000"):
        cpu.step()
    assert cpu.a == 0x12
    assert cpu.x == 0x34
    assert cpu.y == 0x56
    assert cpu.sp == 0x9A
    assert cpu.p == 0xE1
    assert cpu.pc == 0x4000
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


@pytest.mark.parametrize("opcode, initial, operand, expected", [
    # AND
    (0x29, 0xF0, 0x0F, 0x00),
    (0x29, 0xFF, 0x80, 0x80),
    (0x29, 0xAB, 0x3C, 0x28),
    (0x29, 0xFF, 0xFF, 0xFF),
    # ORA
    (0x09, 0x00, 0x00, 0x00),
    (0x09, 0x10, 0x80, 0x90),
    (0x09, 0x21, 0x42, 0x63),
    (0x09, 0xFF, 0x00, 0xFF),
    # EOR
    (0x49, 0xFF, 0xFF, 0x00),
    (0x49, 0x0F, 0x8F, 0x80),
    (0x49, 0xA5, 0x3C, 0x99),
    (0x49, 0xFF, 0x80, 0x7F),
])
def test_immediate_logic_updates_accumulator_and_nz(make_cpu, opcode, initial, operand, expected):
    # Set N and Z opposite to their expected values before the instruction.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, operand)

    # The accumulator and N/Z reflect the bitwise result.
    cpu.step()
    assert cpu.a == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 2


@pytest.mark.parametrize("opcode, register", [(0xC9, "a"), (0xE0, "x"), (0xC0, "y")])
@pytest.mark.parametrize("value, operand, carry, zero, negative", [
    (0x00, 0x00, True, True, False),
    (0x42, 0x42, True, True, False),
    (0x00, 0x01, False, False, True),
    (0x00, 0xFF, False, False, False),
    (0x80, 0x01, True, False, False),
    (0xFF, 0x00, True, False, True),
])
def test_immediate_compare_updates_cnz(make_cpu, opcode, register, value, operand, carry, zero, negative):
    # Start the affected flags opposite to the expected comparison result.
    cpu, machine = make_cpu(start_address=0x0567)
    setattr(cpu, register, value)
    cpu.carry = not carry
    cpu.zero = not zero
    cpu.negative = not negative
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, operand)

    # Comparison updates flags without storing the difference in the source register.
    cpu.step()
    assert getattr(cpu, register) == value
    assert cpu.carry is carry
    assert cpu.zero is zero
    assert cpu.negative is negative
    assert cpu.pc == 0x0569
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


@pytest.mark.parametrize("opcode, register", [(0x85, "a"), (0x86, "x"), (0x84, "y")])
@pytest.mark.parametrize("destination", [0x00, 0xFF])
@pytest.mark.parametrize("value", [0x00, 0x55, 0xFF])
def test_zero_page_stores_write_register(make_cpu, opcode, register, destination, value):
    # Keep instruction bytes separate from the selected zero-page address.
    cpu, machine = make_cpu(start_address=0x0567)
    setattr(cpu, register, value)
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, destination)
    machine.write_byte(destination, value ^ 0xFF)

    # The selected address receives the register byte.
    cpu.step()
    assert machine.read_byte(destination) == value
    assert cpu.pc == 0x0569
    assert cpu.cycles == 3


@pytest.mark.parametrize("opcode, register", [(0xA5, "a"), (0xA6, "x"), (0xA4, "y")])
@pytest.mark.parametrize("source", [0x00, 0xFF])
@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
def test_zero_page_loads_update_register_and_nz(make_cpu, opcode, register, source, value):
    # Start N and Z opposite to their expected values and place data away from the instruction.
    cpu, machine = make_cpu(start_address=0x0567)
    setattr(cpu, register, 0x55)
    cpu.negative = not bool(value & 0x80)
    cpu.zero = value != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, source)
    machine.write_byte(source, value)

    # The selected register and N/Z reflect the addressed byte.
    cpu.step()
    assert getattr(cpu, register) == value
    assert cpu.negative is bool(value & 0x80)
    assert cpu.zero is (value == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 3


@pytest.mark.parametrize("operand, index, pointer_low, pointer_high", [
    (0x20, 0x04, 0x24, 0x25),
    (0xF0, 0x20, 0x10, 0x11),
    (0xFC, 0x03, 0xFF, 0x00),
])
@pytest.mark.parametrize("value", [0x00, 0xA5, 0xFF])
def test_sta_indexed_indirect_writes_accumulator(make_cpu, operand, index, pointer_low, pointer_high, value):
    # Place the instruction and the indexed pointer at separate addresses.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = value
    cpu.x = index
    machine.write_byte(0x0567, 0x81)
    machine.write_byte(0x0568, operand)
    machine.write_byte(pointer_low, 0x45)
    machine.write_byte(pointer_high, 0x03)
    machine.write_byte(0x0345, value ^ 0xFF)

    # The selected pointer resolves to the destination for each wrap case.
    cpu.step()
    assert machine.read_byte(0x0345) == value
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("pointer_low, pointer_high, low, high, index, destination", [
    (0x20, 0x21, 0x30, 0x12, 0x04, 0x1234),
    (0xFF, 0x00, 0xFF, 0x12, 0x01, 0x1300),
    (0x20, 0x21, 0xFF, 0xFF, 0x01, 0x0000),
])
@pytest.mark.parametrize("value", [0x00, 0xA5, 0xFF])
def test_sta_indirect_indexed_writes_accumulator(
    make_cpu, pointer_low, pointer_high, low, high, index, destination, value,
):
    # A zero-page pointer supplies the base address before indexing with Y.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = value
    cpu.y = index
    machine.write_byte(0x0567, 0x91)
    machine.write_byte(0x0568, pointer_low)
    machine.write_byte(pointer_low, low)
    machine.write_byte(pointer_high, high)
    machine.write_byte(destination, value ^ 0xFF)

    # The effective address receives the byte, regardless of page crossing.
    cpu.step()
    assert machine.read_byte(destination) == value
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("opcode, index_register", [(0x9D, "x"), (0x99, "y")])
@pytest.mark.parametrize("base, index, destination", [
    (0x0120, 0x12, 0x0132),
    (0x00FF, 0x01, 0x0100),
    (0xFFFF, 0x01, 0x0000),
])
def test_indexed_absolute_stores_write_accumulator(make_cpu, opcode, index_register, base, index, destination):
    # The program and each indexed destination occupy separate RAM locations.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = 0xA5
    setattr(cpu, index_register, index)
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, base & 0xFF)
    machine.write_byte(0x0569, base >> 8)
    machine.write_byte(destination, 0x5A)

    # The selected address receives A for every page-crossing case.
    cpu.step()
    assert machine.read_byte(destination) == 0xA5
    assert cpu.pc == 0x056A
    assert cpu.cycles == 5


@pytest.mark.parametrize("opcode, register, index_register", [
    (0xBD, "a", "x"), (0xB9, "a", "y"), (0xBE, "x", "y"), (0xBC, "y", "x"),
])
@pytest.mark.parametrize("base, index, source, cycles", [
    (0x0120, 0x12, 0x0132, 4),
    (0x00FF, 0x01, 0x0100, 5),
    (0xFFFF, 0x01, 0x0000, 5),
])
@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
def test_indexed_absolute_loads_update_register_and_nz(
    make_cpu, opcode, register, index_register, base, index, source, cycles, value,
):
    # The index and initial flags distinguish the selected address and loaded value.
    cpu, machine = make_cpu(start_address=0x0567)
    setattr(cpu, register, 0x55)
    setattr(cpu, index_register, index)
    cpu.negative = not bool(value & 0x80)
    cpu.zero = value != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, base & 0xFF)
    machine.write_byte(0x0569, base >> 8)
    machine.write_byte(source, value)

    # The destination and flags reflect the selected byte and page-crossing cost.
    cpu.step()
    assert getattr(cpu, register) == value
    assert cpu.negative is bool(value & 0x80)
    assert cpu.zero is (value == 0)
    assert cpu.pc == 0x056A
    assert cpu.cycles == cycles


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
        (0x40, NotImplementedError, "CPU write at address 0x4000"),
        (0x80, PermissionError, "ROM at offset 0x0000"),
    ],
)
def test_absolute_store_propagates_write_error(make_cpu, opcode, register, high_byte, error, message):
    # Target either unconnected I/O or the beginning of PRG ROM.
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


@pytest.mark.parametrize("failed_pc", [0x0001, 0x4000])
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
