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
    machine.write_byte(0x0567, 0x20)  # JSR opcode
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
    machine.write_byte(0x01FA, 0x20)  # JSR opcode
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
    machine.write_byte(0x0567, 0x60)  # RTS opcode
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
    machine.write_byte(0x0567, 0x0A)  # ASL opcode

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
    machine.write_byte(0x0567, 0x4A)  # LSR opcode

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
    machine.write_byte(0x0567, 0x2A)  # ROL opcode

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
    machine.write_byte(0x0567, 0x6A)  # ROR opcode

    # The rotated byte determines the resulting flags.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0568
    assert cpu.cycles == 2


@pytest.mark.parametrize("opcode, initial, expected", [
    # INC
    (0xEE, 0xFF, 0x00),
    (0xEE, 0x7F, 0x80),
    # DEC
    (0xCE, 0x00, 0xFF),
    (0xCE, 0x01, 0x00),
])
def test_absolute_increment_and_decrement(make_cpu, monkeypatch, opcode, initial, expected):
    # Distinct operand bytes expose little-endian addressing.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)  # INC or DEC opcode
    machine.write_byte(0x0568, 0x34)
    machine.write_byte(0x0569, 0x12)
    machine.write_byte(0x1234, initial)

    # Observe the original and modified writes while preserving real Machine behavior.
    writes = []
    write_byte = machine.write_byte

    def record_write(address, value):
        writes.append((address, value))
        write_byte(address, value)

    monkeypatch.setattr(machine, "write_byte", record_write)

    # The instruction writes the original byte before the incremented value.
    cpu.step()
    assert writes == [(0x1234, initial), (0x1234, expected)]
    assert machine.read_byte(0x1234) == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x056A
    assert cpu.cycles == 6


@pytest.mark.parametrize("opcode, initial, expected, base, index, destination", [
    # INC
    (0xFE, 0xFF, 0x00, 0x00FF, 0x01, 0x0100),
    (0xFE, 0x7F, 0x80, 0x1234, 0x02, 0x1236),
    (0xFE, 0xFE, 0xFF, 0xFFFF, 0x01, 0x0000),
    # DEC
    (0xDE, 0x00, 0xFF, 0x00FF, 0x01, 0x0100),
    (0xDE, 0x01, 0x00, 0x1234, 0x02, 0x1236),
    (0xDE, 0x02, 0x01, 0xFFFF, 0x01, 0x0000),
])
def test_indexed_absolute_increment_and_decrement(
    make_cpu, monkeypatch, opcode, initial, expected, base, index, destination,
):
    # Set X and N/Z before selecting the effective address.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.x = index
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)  # INC or DEC opcode
    machine.write_byte(0x0568, base & 0xFF)
    machine.write_byte(0x0569, base >> 8)
    machine.write_byte(destination, initial)

    # Observe the two writes while preserving real Machine behavior.
    writes = []
    write_byte = machine.write_byte

    def record_write(address, value):
        writes.append((address, value))
        write_byte(address, value)

    monkeypatch.setattr(machine, "write_byte", record_write)

    # The effective address wraps at 16 bits and the instruction always takes seven cycles.
    cpu.step()
    assert writes == [(destination, initial), (destination, expected)]
    assert machine.read_byte(destination) == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x056A
    assert cpu.cycles == 7


@pytest.mark.parametrize("opcode, initial, expected", [
    # INC
    (0xE6, 0x00, 0x01),
    (0xE6, 0x7F, 0x80),
    (0xE6, 0xFE, 0xFF),
    (0xE6, 0xFF, 0x00),
    # DEC
    (0xC6, 0x00, 0xFF),
    (0xC6, 0x01, 0x00),
    (0xC6, 0x80, 0x7F),
    (0xC6, 0x81, 0x80),
])
@pytest.mark.parametrize("destination", [0x00, 0xFF])
def test_zero_page_increment_and_decrement(make_cpu, monkeypatch, opcode, initial, expected, destination):
    # Place the instruction away from the addressed byte and set N/Z opposite to the result.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, destination)
    machine.write_byte(destination, initial)

    # Observe both writes while still forwarding them to Machine.
    writes = []
    write_byte = machine.write_byte

    def record_write(address, value):
        writes.append((address, value))
        write_byte(address, value)

    monkeypatch.setattr(machine, "write_byte", record_write)

    # The original and updated bytes are written in order; N/Z reflect the result.
    cpu.step()
    assert writes == [(destination, initial), (destination, expected)]
    assert machine.read_byte(destination) == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 5


@pytest.mark.parametrize("opcode, initial, expected", [
    # INC
    (0xF6, 0x00, 0x01),
    (0xF6, 0x7F, 0x80),
    (0xF6, 0xFE, 0xFF),
    (0xF6, 0xFF, 0x00),
    # DEC
    (0xD6, 0x00, 0xFF),
    (0xD6, 0x01, 0x00),
    (0xD6, 0x80, 0x7F),
    (0xD6, 0x81, 0x80),
])
@pytest.mark.parametrize("operand, index, destination", [(0x20, 0x04, 0x24), (0xF0, 0x20, 0x10)])
def test_indexed_zero_page_increment_and_decrement(
    make_cpu, monkeypatch, opcode, initial, expected, operand, index, destination,
):
    # Set the index and N/Z before addressing the byte within zero page.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.x = index
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, operand)
    machine.write_byte(destination, initial)

    # Observe both writes while still forwarding them to Machine.
    writes = []
    write_byte = machine.write_byte

    def record_write(address, value):
        writes.append((address, value))
        write_byte(address, value)

    monkeypatch.setattr(machine, "write_byte", record_write)

    # Both writes target the wrapped address and N/Z reflect the updated byte.
    cpu.step()
    assert writes == [(destination, initial), (destination, expected)]
    assert machine.read_byte(destination) == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("opcode, initial, incoming_carry, expected, carry", [
    # ASL
    (0x06, 0x00, False, 0x00, False),
    (0x06, 0x01, True, 0x02, False),
    (0x06, 0x40, False, 0x80, False),
    (0x06, 0x80, True, 0x00, True),
    (0x06, 0xFF, False, 0xFE, True),
    # LSR
    (0x46, 0x00, False, 0x00, False),
    (0x46, 0x01, True, 0x00, True),
    (0x46, 0x02, True, 0x01, False),
    (0x46, 0x80, False, 0x40, False),
    (0x46, 0xFF, False, 0x7F, True),
    # ROL
    (0x26, 0x00, False, 0x00, False),
    (0x26, 0x00, True, 0x01, False),
    (0x26, 0x80, False, 0x00, True),
    (0x26, 0x80, True, 0x01, True),
    (0x26, 0x40, False, 0x80, False),
    (0x26, 0x40, True, 0x81, False),
    (0x26, 0xFF, True, 0xFF, True),
    # ROR
    (0x66, 0x00, False, 0x00, False),
    (0x66, 0x00, True, 0x80, False),
    (0x66, 0x01, False, 0x00, True),
    (0x66, 0x01, True, 0x80, True),
    (0x66, 0x02, False, 0x01, False),
    (0x66, 0x02, True, 0x81, False),
    (0x66, 0xFF, True, 0xFF, True),
])
@pytest.mark.parametrize("destination", [0x00, 0xFF])
def test_zero_page_shift_and_rotate(
    make_cpu, monkeypatch, opcode, initial, incoming_carry, expected, carry, destination,
):
    # Place the instruction away from its zero-page data and set the affected flags.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.carry = incoming_carry
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, destination)
    machine.write_byte(destination, initial)

    # Observe writes while still delegating each one to the connected Machine.
    writes = []
    write_byte = machine.write_byte

    def record_write(address, value):
        writes.append((address, value))
        write_byte(address, value)

    monkeypatch.setattr(machine, "write_byte", record_write)

    # The original and modified bytes are both written in order.
    cpu.step()
    assert writes == [(destination, initial), (destination, expected)]
    assert machine.read_byte(destination) == expected
    assert cpu.carry is carry
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 5


@pytest.mark.parametrize("opcode, initial, incoming_carry, expected, carry", [
    # ASL
    (0x16, 0x00, False, 0x00, False),
    (0x16, 0x01, True, 0x02, False),
    (0x16, 0x40, False, 0x80, False),
    (0x16, 0x80, True, 0x00, True),
    (0x16, 0xFF, False, 0xFE, True),
    # LSR
    (0x56, 0x00, False, 0x00, False),
    (0x56, 0x01, True, 0x00, True),
    (0x56, 0x02, True, 0x01, False),
    (0x56, 0x80, False, 0x40, False),
    (0x56, 0xFF, False, 0x7F, True),
    # ROL
    (0x36, 0x00, False, 0x00, False),
    (0x36, 0x00, True, 0x01, False),
    (0x36, 0x80, False, 0x00, True),
    (0x36, 0x80, True, 0x01, True),
    (0x36, 0x40, False, 0x80, False),
    (0x36, 0x40, True, 0x81, False),
    (0x36, 0xFF, True, 0xFF, True),
    # ROR
    (0x76, 0x00, False, 0x00, False),
    (0x76, 0x00, True, 0x80, False),
    (0x76, 0x01, False, 0x00, True),
    (0x76, 0x01, True, 0x80, True),
    (0x76, 0x02, False, 0x01, False),
    (0x76, 0x02, True, 0x81, False),
    (0x76, 0xFF, True, 0xFF, True),
])
@pytest.mark.parametrize("operand, index, destination", [
    (0x20, 0x04, 0x24),
    (0xF0, 0x20, 0x10),
    (0xFC, 0x03, 0xFF),
])
def test_indexed_zero_page_shift_and_rotate(
    make_cpu, monkeypatch, opcode, initial, incoming_carry, expected, carry, operand, index, destination,
):
    # Set X and the affected flags before addressing the byte in zero page.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.x = index
    cpu.carry = incoming_carry
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, operand)
    machine.write_byte(destination, initial)

    # Observe both writes while still forwarding them to Machine.
    writes = []
    write_byte = machine.write_byte

    def record_write(address, value):
        writes.append((address, value))
        write_byte(address, value)

    monkeypatch.setattr(machine, "write_byte", record_write)

    # Both writes target the wrapped address and C/N/Z reflect the result.
    cpu.step()
    assert writes == [(destination, initial), (destination, expected)]
    assert machine.read_byte(destination) == expected
    assert cpu.carry is carry
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("opcode, initial, incoming_carry, expected, carry", [
    # ASL
    (0x0E, 0x00, False, 0x00, False),
    (0x0E, 0x01, True, 0x02, False),
    (0x0E, 0x40, False, 0x80, False),
    (0x0E, 0x80, True, 0x00, True),
    (0x0E, 0xFF, False, 0xFE, True),
    # LSR
    (0x4E, 0x00, False, 0x00, False),
    (0x4E, 0x01, True, 0x00, True),
    (0x4E, 0x02, True, 0x01, False),
    (0x4E, 0x80, False, 0x40, False),
    (0x4E, 0xFF, False, 0x7F, True),
    # ROL
    (0x2E, 0x00, False, 0x00, False),
    (0x2E, 0x00, True, 0x01, False),
    (0x2E, 0x80, False, 0x00, True),
    (0x2E, 0x80, True, 0x01, True),
    (0x2E, 0x40, False, 0x80, False),
    (0x2E, 0x40, True, 0x81, False),
    (0x2E, 0xFF, True, 0xFF, True),
    # ROR
    (0x6E, 0x00, False, 0x00, False),
    (0x6E, 0x00, True, 0x80, False),
    (0x6E, 0x01, False, 0x00, True),
    (0x6E, 0x01, True, 0x80, True),
    (0x6E, 0x02, False, 0x01, False),
    (0x6E, 0x02, True, 0x81, False),
    (0x6E, 0xFF, True, 0xFF, True),
])
def test_absolute_shift_and_rotate(make_cpu, monkeypatch, opcode, initial, incoming_carry, expected, carry):
    # Use distinct address bytes and set C/N/Z before executing the instruction.
    cpu, machine = make_cpu(start_address=0x0200)
    cpu.carry = incoming_carry
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0200, opcode)
    machine.write_byte(0x0201, 0x56)
    machine.write_byte(0x0202, 0x04)
    machine.write_byte(0x0456, initial)

    # Observe writes while still delegating each one to the connected Machine.
    writes = []
    write_byte = machine.write_byte

    def record_write(address, value):
        writes.append((address, value))
        write_byte(address, value)

    monkeypatch.setattr(machine, "write_byte", record_write)

    # Both writes occur in order and the final byte determines C/N/Z.
    cpu.step()
    assert writes == [(0x0456, initial), (0x0456, expected)]
    assert machine.read_byte(0x0456) == expected
    assert cpu.carry is carry
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0203
    assert cpu.cycles == 6


@pytest.mark.parametrize("opcode, initial, incoming_carry, expected, carry", [
    # ASL
    (0x1E, 0x00, False, 0x00, False),
    (0x1E, 0x01, True, 0x02, False),
    (0x1E, 0x40, False, 0x80, False),
    (0x1E, 0x80, True, 0x00, True),
    (0x1E, 0xFF, False, 0xFE, True),
    # LSR
    (0x5E, 0x00, False, 0x00, False),
    (0x5E, 0x01, True, 0x00, True),
    (0x5E, 0x02, True, 0x01, False),
    (0x5E, 0x80, False, 0x40, False),
    (0x5E, 0xFF, False, 0x7F, True),
    # ROL
    (0x3E, 0x00, False, 0x00, False),
    (0x3E, 0x00, True, 0x01, False),
    (0x3E, 0x80, False, 0x00, True),
    (0x3E, 0x80, True, 0x01, True),
    (0x3E, 0x40, False, 0x80, False),
    (0x3E, 0x40, True, 0x81, False),
    (0x3E, 0xFF, True, 0xFF, True),
    # ROR
    (0x7E, 0x00, False, 0x00, False),
    (0x7E, 0x00, True, 0x80, False),
    (0x7E, 0x01, False, 0x00, True),
    (0x7E, 0x01, True, 0x80, True),
    (0x7E, 0x02, False, 0x01, False),
    (0x7E, 0x02, True, 0x81, False),
    (0x7E, 0xFF, True, 0xFF, True),
])
@pytest.mark.parametrize("base, index, destination", [
    (0x0120, 0x12, 0x0132),
    (0x00FF, 0x01, 0x0100),
    (0xFFFF, 0x01, 0x0000),
])
def test_indexed_absolute_shift_and_rotate(
    make_cpu, monkeypatch, opcode, initial, incoming_carry, expected, carry, base, index, destination,
):
    # Set the indexed address and the affected flags before the instruction.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.x = index
    cpu.carry = incoming_carry
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, base & 0xFF)
    machine.write_byte(0x0569, base >> 8)
    machine.write_byte(destination, initial)

    # Observe writes while still delegating each one to the connected Machine.
    writes = []
    write_byte = machine.write_byte

    def record_write(address, value):
        writes.append((address, value))
        write_byte(address, value)

    monkeypatch.setattr(machine, "write_byte", record_write)

    # Both writes target the indexed address and always take seven cycles.
    cpu.step()
    assert writes == [(destination, initial), (destination, expected)]
    assert machine.read_byte(destination) == expected
    assert cpu.carry is carry
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x056A
    assert cpu.cycles == 7


def test_jmp_absolute_loads_destination(make_cpu):
    # An asymmetric target exposes reversed operand bytes.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x4C)  # JMP opcode
    machine.write_byte(0x0001, 0x34)
    machine.write_byte(0x0002, 0x12)

    # The destination becomes PC without fetching an instruction there.
    cpu.step()
    assert cpu.pc == 0x1234
    assert cpu.cycles == 3


def test_jmp_indirect_loads_destination(make_cpu):
    # Distinct pointer and target bytes expose incorrect address or byte order.
    cpu, machine = make_cpu(start_address=0x0200)
    machine.write_byte(0x0200, 0x6C)  # JMP opcode
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
    machine.write_byte(0x0400, 0x6C)  # JMP opcode
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
    machine.write_byte(0x0200, 0x6C)  # JMP opcode
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
    machine.write_byte(0x0000, 0x78)  # SEI opcode
    cpu.interrupt_disable = initial_i

    # SEI sets I from either initial value.
    cpu.step()
    assert cpu.interrupt_disable is True
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_i", [False, True])
def test_step_cli_clears_interrupt_disable(make_cpu, initial_i):
    # Place CLI at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x58)  # CLI opcode
    cpu.interrupt_disable = initial_i

    # CLI clears I from either initial value.
    cpu.step()
    assert cpu.interrupt_disable is False
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_c", [False, True])
def test_step_clc_clears_carry(make_cpu, initial_c):
    # Place CLC at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x18)  # CLC opcode
    cpu.carry = initial_c

    # CLC clears C from either initial value.
    cpu.step()
    assert cpu.carry is False
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_c", [False, True])
def test_step_sec_sets_carry(make_cpu, initial_c):
    # Place SEC at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0x38)  # SEC opcode
    cpu.carry = initial_c

    # SEC sets C from either initial value.
    cpu.step()
    assert cpu.carry is True
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_d", [False, True])
def test_step_cld_clears_decimal_flag(make_cpu, initial_d):
    # Place CLD at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xD8)  # CLD opcode
    cpu.decimal = initial_d

    # CLD clears D from either initial value.
    cpu.step()
    assert cpu.decimal is False
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_d", [False, True])
def test_step_sed_sets_decimal_flag(make_cpu, initial_d):
    # Place SED at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xF8)  # SED opcode
    cpu.decimal = initial_d

    # SED sets D from either initial value.
    cpu.step()
    assert cpu.decimal is True
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial_v", [False, True])
def test_step_clv_clears_overflow(make_cpu, initial_v):
    # Place CLV at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xB8)  # CLV opcode
    cpu.overflow = initial_v

    # CLV clears V from either initial value.
    cpu.step()
    assert cpu.overflow is False
    assert cpu.cycles == 2


def test_step_nop_advances_pc(make_cpu):
    # Place the official one-byte NOP at the default reset address in RAM.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xEA)  # NOP opcode

    # The opcode fetch advances PC by one byte.
    cpu.step()
    assert cpu.pc == 0x0001
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, False, 0x00, False, False),
    (0x00, 0x00, True, 0x01, False, False),
    (0x7F, 0x01, False, 0x80, False, True),
    (0x80, 0x80, False, 0x00, True, True),
    (0xFF, 0x00, True, 0x00, True, False),
    (0x80, 0x7F, False, 0xFF, False, False),
    (0x09, 0x01, False, 0x0A, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("source, index, destination", [(0x20, 0x04, 0x24), (0xF0, 0x20, 0x10)])
def test_adc_zero_page_indexed(
    make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal, source, index, destination,
):
    # Set X and the affected flags before addressing the byte in zero page.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.x = index
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0x75)  # ADC opcode
    machine.write_byte(0x0568, source)
    machine.write_byte(destination, operand)

    # A and C/V/N/Z reflect binary addition from the indexed address.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == 4


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, False, 0x00, False, False),
    (0x00, 0x00, True, 0x01, False, False),
    (0x7F, 0x01, False, 0x80, False, True),
    (0x80, 0x80, False, 0x00, True, True),
    (0xFF, 0x00, True, 0x00, True, False),
    (0x80, 0x7F, False, 0xFF, False, False),
    (0x09, 0x01, False, 0x0A, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("opcode, index_register", [
    (0x7D, "x"),  # ADC absolute,X
    (0x79, "y"),  # ADC absolute,Y
])
@pytest.mark.parametrize("base, index, source, cycles", [
    (0x0120, 0x12, 0x0132, 4),
    (0x00FF, 0x01, 0x0100, 5),
    (0xFFFF, 0x01, 0x0000, 5),
])
def test_adc_absolute_indexed(
    make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal, opcode, index_register,
    base, index, source, cycles,
):
    # Set the index and flags before addressing the byte in RAM.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    setattr(cpu, index_register, index)
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, base & 0xFF)
    machine.write_byte(0x0569, base >> 8)
    machine.write_byte(source, operand)

    # A and C/V/N/Z reflect binary addition and the indexed access determines cycles.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x056A
    assert cpu.cycles == cycles


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, False, 0x00, False, False),
    (0x00, 0x00, True, 0x01, False, False),
    (0x7F, 0x01, False, 0x80, False, True),
    (0x80, 0x80, False, 0x00, True, True),
    (0xFF, 0x00, True, 0x00, True, False),
    (0x80, 0x7F, False, 0xFF, False, False),
    (0x09, 0x01, False, 0x0A, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
def test_adc_absolute(make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal):
    # Use distinct address bytes and set the affected flags for a binary addition.
    cpu, machine = make_cpu(start_address=0x0200)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0200, 0x6D)  # ADC opcode
    machine.write_byte(0x0201, 0x56)
    machine.write_byte(0x0202, 0x04)
    machine.write_byte(0x0456, operand)

    # A and C/V/N/Z reflect the addressed byte regardless of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0203
    assert cpu.cycles == 4


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, False, 0x00, False, False),
    (0x00, 0x00, True, 0x01, False, False),
    (0x7F, 0x00, True, 0x80, False, True),
    (0x7F, 0x01, False, 0x80, False, True),
    (0x80, 0x80, False, 0x00, True, True),
    (0xFF, 0x00, True, 0x00, True, False),
    (0x80, 0x7F, False, 0xFF, False, False),
    (0x09, 0x01, False, 0x0A, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("source", [0x00, 0xFF])
def test_adc_zero_page(make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal, source):
    # The instruction points to one endpoint of zero page.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0x65)  # ADC opcode
    machine.write_byte(0x0568, source)
    machine.write_byte(source, operand)

    # A and C/V/N/Z reflect binary addition regardless of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == 3


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, False, 0x00, False, False),
    (0x00, 0x00, True, 0x01, False, False),
    (0x7F, 0x00, True, 0x80, False, True),
    (0x7F, 0x01, False, 0x80, False, True),
    (0x80, 0x80, False, 0x00, True, True),
    (0xFF, 0x00, True, 0x00, True, False),
    (0xFF, 0xFF, True, 0xFF, True, False),
    (0x80, 0x7F, False, 0xFF, False, False),
    (0x09, 0x01, False, 0x0A, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
def test_adc_immediate(make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal):
    # Set the relevant flags and place each instruction byte in RAM.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0x69)  # ADC opcode
    machine.write_byte(0x0568, operand)

    # Binary addition updates A and C/V/N/Z independently of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, True, 0x00, True, False),
    (0x00, 0x00, False, 0xFF, False, False),
    (0x00, 0x01, True, 0xFF, False, False),
    (0x80, 0x01, True, 0x7F, True, True),
    (0x7F, 0xFF, True, 0x80, False, True),
    (0x42, 0x42, True, 0x00, True, False),
    (0x10, 0x01, True, 0x0F, True, False),
    (0x00, 0xFF, False, 0x00, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("source, index, destination", [(0x20, 0x04, 0x24), (0xF0, 0x20, 0x10)])
def test_sbc_zero_page_indexed(
    make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal, source, index, destination,
):
    # Set X and the affected flags before addressing the byte in zero page.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.x = index
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0xF5)  # SBC opcode
    machine.write_byte(0x0568, source)
    machine.write_byte(destination, operand)

    # A and C/V/N/Z reflect binary subtraction from the indexed address.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == 4


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, True, 0x00, True, False),
    (0x00, 0x00, False, 0xFF, False, False),
    (0x00, 0x01, True, 0xFF, False, False),
    (0x80, 0x01, True, 0x7F, True, True),
    (0x7F, 0xFF, True, 0x80, False, True),
    (0x42, 0x42, True, 0x00, True, False),
    (0x10, 0x01, True, 0x0F, True, False),
    (0x00, 0xFF, False, 0x00, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("opcode, index_register", [
    (0xFD, "x"),  # SBC absolute,X
    (0xF9, "y"),  # SBC absolute,Y
])
@pytest.mark.parametrize("base, index, source, cycles", [
    (0x0120, 0x12, 0x0132, 4),
    (0x00FF, 0x01, 0x0100, 5),
    (0xFFFF, 0x01, 0x0000, 5),
])
def test_sbc_absolute_indexed(
    make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal, opcode, index_register,
    base, index, source, cycles,
):
    # Set the index and flags before addressing the byte in RAM.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    setattr(cpu, index_register, index)
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, base & 0xFF)
    machine.write_byte(0x0569, base >> 8)
    machine.write_byte(source, operand)

    # A and C/V/N/Z reflect binary subtraction and the indexed access determines cycles.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x056A
    assert cpu.cycles == cycles


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, True, 0x00, True, False),
    (0x00, 0x00, False, 0xFF, False, False),
    (0x00, 0x01, True, 0xFF, False, False),
    (0x80, 0x01, True, 0x7F, True, True),
    (0x7F, 0xFF, True, 0x80, False, True),
    (0x42, 0x42, True, 0x00, True, False),
    (0x10, 0x01, True, 0x0F, True, False),
    (0x00, 0xFF, False, 0x00, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
def test_sbc_absolute(make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal):
    # Use distinct address bytes and set the affected flags for a binary subtraction.
    cpu, machine = make_cpu(start_address=0x0200)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0200, 0xED)  # SBC opcode
    machine.write_byte(0x0201, 0x56)
    machine.write_byte(0x0202, 0x04)
    machine.write_byte(0x0456, operand)

    # A and C/V/N/Z reflect the addressed byte regardless of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0203
    assert cpu.cycles == 4


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, True, 0x00, True, False),
    (0x00, 0x00, False, 0xFF, False, False),
    (0x00, 0x01, True, 0xFF, False, False),
    (0x80, 0x01, True, 0x7F, True, True),
    (0x7F, 0xFF, True, 0x80, False, True),
    (0x42, 0x42, True, 0x00, True, False),
    (0x10, 0x01, True, 0x0F, True, False),
    (0xFF, 0x00, True, 0xFF, True, False),
    (0x00, 0xFF, False, 0x00, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
def test_sbc_immediate(make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal):
    # Set the relevant flags and place each instruction byte in RAM.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0xE9)  # SBC opcode
    machine.write_byte(0x0568, operand)

    # Binary subtraction updates A and C/V/N/Z independently of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == 2


@pytest.mark.parametrize("initial, operand, incoming_carry, expected, carry, overflow", [
    (0x00, 0x00, True, 0x00, True, False),
    (0x00, 0x00, False, 0xFF, False, False),
    (0x00, 0x01, True, 0xFF, False, False),
    (0x80, 0x01, True, 0x7F, True, True),
    (0x7F, 0xFF, True, 0x80, False, True),
    (0x42, 0x42, True, 0x00, True, False),
    (0x10, 0x01, True, 0x0F, True, False),
    (0x00, 0xFF, False, 0x00, False, False),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("source", [0x00, 0xFF])
def test_sbc_zero_page(make_cpu, initial, operand, incoming_carry, expected, carry, overflow, decimal, source):
    # The instruction points to one endpoint of zero page.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0xE5)  # SBC opcode
    machine.write_byte(0x0568, source)
    machine.write_byte(source, operand)

    # A and C/V/N/Z reflect binary subtraction regardless of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == 3


@pytest.mark.parametrize("opcode, initial, value, expected", [
    # AND (zp,X)
    (0x21, 0xF0, 0x0F, 0x00),
    (0x21, 0xFF, 0x80, 0x80),
    # ORA (zp,X)
    (0x01, 0x00, 0x00, 0x00),
    (0x01, 0x35, 0xCA, 0xFF),
    # EOR (zp,X)
    (0x41, 0xFF, 0xFF, 0x00),
    (0x41, 0x7F, 0xFF, 0x80),
])
@pytest.mark.parametrize("operand, index, pointer_low, pointer_high", [
    (0x20, 0x04, 0x24, 0x25),
    (0xF0, 0x20, 0x10, 0x11),
    (0xFC, 0x03, 0xFF, 0x00),
])
def test_indexed_indirect_logic_updates_accumulator_and_nz(
    make_cpu, opcode, initial, value, expected, operand, index, pointer_low, pointer_high,
):
    # Place the instruction, wrapping pointer, and source in separate RAM locations.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.x = index
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, operand)
    machine.write_byte(pointer_low, 0x34)
    machine.write_byte(pointer_high, 0x02)
    machine.write_byte(0x0234, value)

    # The selected byte determines A and N/Z in six cycles.
    cpu.step()
    assert cpu.a == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("opcode, initial, value, expected", [
    # AND (zp),Y
    (0x31, 0xF0, 0x0F, 0x00),
    (0x31, 0xFF, 0x80, 0x80),
    # ORA (zp),Y
    (0x11, 0x00, 0x00, 0x00),
    (0x11, 0x35, 0xCA, 0xFF),
    # EOR (zp),Y
    (0x51, 0xFF, 0xFF, 0x00),
    (0x51, 0x7F, 0xFF, 0x80),
])
@pytest.mark.parametrize("pointer_low, pointer_high, low, high, index, source, cycles", [
    (0x20, 0x21, 0x30, 0x02, 0x04, 0x0234, 5),
    (0xFF, 0x00, 0xFF, 0x02, 0x01, 0x0300, 6),
    (0x20, 0x21, 0xFF, 0xFF, 0x01, 0x0000, 6),
])
def test_indirect_indexed_logic_updates_accumulator_and_nz(
    make_cpu, opcode, initial, value, expected, pointer_low, pointer_high, low, high, index, source, cycles,
):
    # A zero-page pointer supplies the base before indexing with Y.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.y = index
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, pointer_low)
    machine.write_byte(pointer_low, low)
    machine.write_byte(pointer_high, high)
    machine.write_byte(source, value)

    # A and N/Z reflect the byte, with an extra cycle when the page changes.
    cpu.step()
    assert cpu.a == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == cycles


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


@pytest.mark.parametrize("opcode, initial, operand, expected", [
    # AND
    (0x25, 0xF0, 0x0F, 0x00),
    (0x25, 0xFF, 0x80, 0x80),
    (0x25, 0xAB, 0x3C, 0x28),
    (0x25, 0xFF, 0xFF, 0xFF),
    # ORA
    (0x05, 0x00, 0x00, 0x00),
    (0x05, 0x10, 0x80, 0x90),
    (0x05, 0x21, 0x42, 0x63),
    (0x05, 0xFF, 0x00, 0xFF),
    # EOR
    (0x45, 0xFF, 0xFF, 0x00),
    (0x45, 0x0F, 0x8F, 0x80),
    (0x45, 0xA5, 0x3C, 0x99),
    (0x45, 0xFF, 0x80, 0x7F),
])
@pytest.mark.parametrize("source", [0x00, 0xFF])
def test_zero_page_logic_updates_accumulator_and_nz(make_cpu, opcode, initial, operand, expected, source):
    # Set the data and instruction at separate addresses, with flags opposite to their expected values.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, source)
    machine.write_byte(source, operand)

    # A and N/Z reflect the bitwise result read from zero page.
    cpu.step()
    assert cpu.a == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 3


@pytest.mark.parametrize("opcode, initial, operand, expected", [
    # AND
    (0x35, 0xF0, 0x0F, 0x00),
    (0x35, 0xFF, 0x80, 0x80),
    (0x35, 0xAB, 0x3C, 0x28),
    (0x35, 0xFF, 0xFF, 0xFF),
    # ORA
    (0x15, 0x00, 0x00, 0x00),
    (0x15, 0x10, 0x80, 0x90),
    (0x15, 0x21, 0x42, 0x63),
    (0x15, 0xFF, 0x00, 0xFF),
    # EOR
    (0x55, 0xFF, 0xFF, 0x00),
    (0x55, 0x0F, 0x8F, 0x80),
    (0x55, 0xA5, 0x3C, 0x99),
    (0x55, 0xFF, 0x80, 0x7F),
])
@pytest.mark.parametrize("base, index, source", [(0x20, 0x04, 0x24), (0xF0, 0x20, 0x10), (0xFC, 0x03, 0xFF)])
def test_indexed_zero_page_logic_updates_accumulator_and_nz(
    make_cpu, opcode, initial, operand, expected, base, index, source,
):
    # Set X and start N/Z opposite to the expected result.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.x = index
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, base)
    machine.write_byte(source, operand)

    # A and N/Z reflect the indexed zero-page byte.
    cpu.step()
    assert cpu.a == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 4


@pytest.mark.parametrize("opcode, initial, operand, expected", [
    # AND
    (0x2D, 0xF0, 0x0F, 0x00),
    (0x2D, 0xFF, 0x80, 0x80),
    (0x2D, 0xAB, 0x3C, 0x28),
    (0x2D, 0xFF, 0xFF, 0xFF),
    # ORA
    (0x0D, 0x00, 0x00, 0x00),
    (0x0D, 0x10, 0x80, 0x90),
    (0x0D, 0x21, 0x42, 0x63),
    (0x0D, 0xFF, 0x00, 0xFF),
    # EOR
    (0x4D, 0xFF, 0xFF, 0x00),
    (0x4D, 0x0F, 0x8F, 0x80),
    (0x4D, 0xA5, 0x3C, 0x99),
    (0x4D, 0xFF, 0x80, 0x7F),
])
def test_absolute_logic_updates_accumulator_and_nz(make_cpu, opcode, initial, operand, expected):
    # Use distinct address bytes and start N/Z opposite to their expected values.
    cpu, machine = make_cpu(start_address=0x0200)
    cpu.a = initial
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0200, opcode)
    machine.write_byte(0x0201, 0x56)
    machine.write_byte(0x0202, 0x04)
    machine.write_byte(0x0456, operand)

    # A and N/Z reflect the result read from the selected address.
    cpu.step()
    assert cpu.a == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x0203
    assert cpu.cycles == 4


@pytest.mark.parametrize("opcode, index_register, initial, operand, expected", [
    # AND absolute,X
    (0x3D, "x", 0xF0, 0x0F, 0x00),
    (0x3D, "x", 0xFF, 0x80, 0x80),
    (0x3D, "x", 0xAB, 0x3C, 0x28),
    (0x3D, "x", 0xFF, 0xFF, 0xFF),
    # AND absolute,Y
    (0x39, "y", 0xF0, 0x0F, 0x00),
    (0x39, "y", 0xFF, 0x80, 0x80),
    (0x39, "y", 0xAB, 0x3C, 0x28),
    (0x39, "y", 0xFF, 0xFF, 0xFF),
    # ORA absolute,X
    (0x1D, "x", 0x00, 0x00, 0x00),
    (0x1D, "x", 0x10, 0x80, 0x90),
    (0x1D, "x", 0x21, 0x42, 0x63),
    (0x1D, "x", 0xFF, 0x00, 0xFF),
    # ORA absolute,Y
    (0x19, "y", 0x00, 0x00, 0x00),
    (0x19, "y", 0x10, 0x80, 0x90),
    (0x19, "y", 0x21, 0x42, 0x63),
    (0x19, "y", 0xFF, 0x00, 0xFF),
    # EOR absolute,X
    (0x5D, "x", 0xFF, 0xFF, 0x00),
    (0x5D, "x", 0x0F, 0x8F, 0x80),
    (0x5D, "x", 0xA5, 0x3C, 0x99),
    (0x5D, "x", 0xFF, 0x80, 0x7F),
    # EOR absolute,Y
    (0x59, "y", 0xFF, 0xFF, 0x00),
    (0x59, "y", 0x0F, 0x8F, 0x80),
    (0x59, "y", 0xA5, 0x3C, 0x99),
    (0x59, "y", 0xFF, 0x80, 0x7F),
])
@pytest.mark.parametrize("base, index, source, cycles", [
    (0x0120, 0x12, 0x0132, 4),
    (0x00FF, 0x01, 0x0100, 5),
    (0xFFFF, 0x01, 0x0000, 5),
])
def test_indexed_absolute_logic_updates_accumulator_and_nz(
    make_cpu, opcode, index_register, initial, operand, expected, base, index, source, cycles,
):
    # Address the test byte with X or Y and start N/Z opposite to the expected values.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    setattr(cpu, index_register, index)
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, base & 0xFF)
    machine.write_byte(0x0569, base >> 8)
    machine.write_byte(source, operand)

    # A and N/Z reflect the indexed byte, with a cycle added on page crossing.
    cpu.step()
    assert cpu.a == expected
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.pc == 0x056A
    assert cpu.cycles == cycles


@pytest.mark.parametrize("accumulator, operand, negative, overflow, zero", [
    (0x40, 0x80, True, False, True),
    (0x40, 0x40, False, True, False),
    (0x00, 0xC0, True, True, True),
    (0x0F, 0x01, False, False, False),
    (0x0F, 0x00, False, False, True),
    (0x80, 0x80, True, False, False),
])
@pytest.mark.parametrize("source", [0x00, 0xFF])
def test_bit_zero_page(make_cpu, accumulator, operand, negative, overflow, zero, source):
    # Set N/V/Z opposite to the expected result and place data away from the program.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = accumulator
    cpu.negative = not negative
    cpu.overflow = not overflow
    cpu.zero = not zero
    machine.write_byte(0x0567, 0x24)  # BIT opcode
    machine.write_byte(0x0568, source)
    machine.write_byte(source, operand)

    # BIT preserves A and sets N/V from memory and Z from A AND memory.
    cpu.step()
    assert cpu.a == accumulator
    assert cpu.negative is negative
    assert cpu.overflow is overflow
    assert cpu.zero is zero
    assert cpu.pc == 0x0569
    assert cpu.cycles == 3


@pytest.mark.parametrize("accumulator, operand, negative, overflow, zero", [
    (0x40, 0x80, True, False, True),
    (0x40, 0x40, False, True, False),
    (0x00, 0xC0, True, True, True),
    (0x0F, 0x01, False, False, False),
    (0x0F, 0x00, False, False, True),
    (0x80, 0x80, True, False, False),
])
def test_bit_absolute(make_cpu, accumulator, operand, negative, overflow, zero):
    # Use distinct address bytes and set N/V/Z opposite to the expected result.
    cpu, machine = make_cpu(start_address=0x0200)
    cpu.a = accumulator
    cpu.negative = not negative
    cpu.overflow = not overflow
    cpu.zero = not zero
    machine.write_byte(0x0200, 0x2C)  # BIT opcode
    machine.write_byte(0x0201, 0x56)
    machine.write_byte(0x0202, 0x04)
    machine.write_byte(0x0456, operand)

    # BIT preserves A and sets N/V from memory and Z from A AND memory.
    cpu.step()
    assert cpu.a == accumulator
    assert cpu.negative is negative
    assert cpu.overflow is overflow
    assert cpu.zero is zero
    assert cpu.pc == 0x0203
    assert cpu.cycles == 4


@pytest.mark.parametrize("opcode, register", [
    (0xC9, "a"),  # CMP immediate
    (0xE0, "x"),  # CPX immediate
    (0xC0, "y"),  # CPY immediate
])
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


@pytest.mark.parametrize("opcode, register", [
    (0xC5, "a"),  # CMP zero page
    (0xE4, "x"),  # CPX zero page
    (0xC4, "y"),  # CPY zero page
])
@pytest.mark.parametrize("source", [0x00, 0xFF])
@pytest.mark.parametrize("value, operand, carry, zero, negative", [
    (0x00, 0x00, True, True, False),
    (0x42, 0x42, True, True, False),
    (0x00, 0x01, False, False, True),
    (0x00, 0xFF, False, False, False),
    (0x80, 0x01, True, False, False),
    (0xFF, 0x00, True, False, True),
])
def test_zero_page_compare_updates_cnz(make_cpu, opcode, register, source, value, operand, carry, zero, negative):
    # Start C/N/Z opposite to the result and keep data away from the instruction.
    cpu, machine = make_cpu(start_address=0x0567)
    setattr(cpu, register, value)
    cpu.carry = not carry
    cpu.zero = not zero
    cpu.negative = not negative
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, source)
    machine.write_byte(source, operand)

    # The comparison preserves the source register and updates C/N/Z.
    cpu.step()
    assert getattr(cpu, register) == value
    assert cpu.carry is carry
    assert cpu.zero is zero
    assert cpu.negative is negative
    assert cpu.pc == 0x0569
    assert cpu.cycles == 3


@pytest.mark.parametrize("source, index, destination", [(0x20, 0x04, 0x24), (0xF0, 0x20, 0x10)])
@pytest.mark.parametrize("value, operand, carry, zero, negative", [
    (0x00, 0x00, True, True, False),
    (0x42, 0x42, True, True, False),
    (0x00, 0x01, False, False, True),
    (0x00, 0xFF, False, False, False),
    (0x80, 0x01, True, False, False),
    (0xFF, 0x00, True, False, True),
])
def test_cmp_indexed_zero_page_updates_cnz(
    make_cpu, source, index, destination, value, operand, carry, zero, negative,
):
    # Set X and start C/N/Z opposite to the expected comparison result.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = value
    cpu.x = index
    cpu.carry = not carry
    cpu.zero = not zero
    cpu.negative = not negative
    machine.write_byte(0x0567, 0xD5)  # CMP zero page,X
    machine.write_byte(0x0568, source)
    machine.write_byte(destination, operand)

    # The flags reflect the byte at the wrapped zero-page address.
    cpu.step()
    assert cpu.a == value
    assert cpu.carry is carry
    assert cpu.zero is zero
    assert cpu.negative is negative
    assert cpu.pc == 0x0569
    assert cpu.cycles == 4


@pytest.mark.parametrize("opcode, register", [
    (0xCD, "a"),  # CMP absolute
    (0xEC, "x"),  # CPX absolute
    (0xCC, "y"),  # CPY absolute
])
@pytest.mark.parametrize("value, operand, carry, zero, negative", [
    (0x00, 0x00, True, True, False),
    (0x42, 0x42, True, True, False),
    (0x00, 0x01, False, False, True),
    (0x00, 0xFF, False, False, False),
    (0x80, 0x01, True, False, False),
    (0xFF, 0x00, True, False, True),
])
def test_absolute_compare_updates_cnz(make_cpu, opcode, register, value, operand, carry, zero, negative):
    # Use distinct address bytes and start the affected flags opposite to the expected result.
    cpu, machine = make_cpu(start_address=0x0200)
    setattr(cpu, register, value)
    cpu.carry = not carry
    cpu.zero = not zero
    cpu.negative = not negative
    machine.write_byte(0x0200, opcode)
    machine.write_byte(0x0201, 0x56)
    machine.write_byte(0x0202, 0x04)
    machine.write_byte(0x0456, operand)

    # Comparison changes C/N/Z without storing the difference in the register.
    cpu.step()
    assert getattr(cpu, register) == value
    assert cpu.carry is carry
    assert cpu.zero is zero
    assert cpu.negative is negative
    assert cpu.pc == 0x0203
    assert cpu.cycles == 4


@pytest.mark.parametrize("opcode, index_register", [
    (0xDD, "x"),  # CMP absolute,X
    (0xD9, "y"),  # CMP absolute,Y
])
@pytest.mark.parametrize("base, index, source, cycles", [
    (0x0120, 0x12, 0x0132, 4),
    (0x00FF, 0x01, 0x0100, 5),
    (0xFFFF, 0x01, 0x0000, 5),
])
@pytest.mark.parametrize("value, operand, carry, zero, negative", [
    (0x00, 0x00, True, True, False),
    (0x42, 0x42, True, True, False),
    (0x00, 0x01, False, False, True),
    (0x00, 0xFF, False, False, False),
    (0x80, 0x01, True, False, False),
    (0xFF, 0x00, True, False, True),
])
def test_cmp_indexed_absolute_updates_cnz(
    make_cpu, opcode, index_register, base, index, source, cycles, value, operand, carry, zero, negative,
):
    # Compare A with data at the indexed address, starting with opposite flags.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = value
    setattr(cpu, index_register, index)
    cpu.carry = not carry
    cpu.zero = not zero
    cpu.negative = not negative
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, base & 0xFF)
    machine.write_byte(0x0569, base >> 8)
    machine.write_byte(source, operand)

    # The flags reflect the selected byte and cycles include any page crossing.
    cpu.step()
    assert cpu.a == value
    assert cpu.carry is carry
    assert cpu.zero is zero
    assert cpu.negative is negative
    assert cpu.pc == 0x056A
    assert cpu.cycles == cycles


@pytest.mark.parametrize("opcode, register", [
    (0xA9, "a"),  # LDA immediate
    (0xA2, "x"),  # LDX immediate
    (0xA0, "y"),  # LDY immediate
])
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


@pytest.mark.parametrize("opcode, register", [
    (0x85, "a"),  # STA zero page
    (0x86, "x"),  # STX zero page
    (0x84, "y"),  # STY zero page
])
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


@pytest.mark.parametrize("opcode, register, index_register", [
    (0x95, "a", "x"),  # STA zero page,X
    (0x96, "x", "y"),  # STX zero page,Y
    (0x94, "y", "x"),  # STY zero page,X
])
@pytest.mark.parametrize("operand, index, destination", [(0x20, 0x04, 0x24), (0xF0, 0x20, 0x10)])
@pytest.mark.parametrize("value", [0x00, 0xA5, 0xFF])
@pytest.mark.parametrize("flags", [0x20, 0xFF])
def test_indexed_zero_page_stores(make_cpu, opcode, register, index_register, operand, index, destination, value, flags):
    # Keep the instruction separate from indexed zero-page data.
    cpu, machine = make_cpu(start_address=0x0567)
    setattr(cpu, register, value)
    setattr(cpu, index_register, index)
    cpu.p = flags
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, operand)
    machine.write_byte(destination, value ^ 0xFF)

    # Stores preserve flags and write to the wrapped address.
    cpu.step()
    assert machine.read_byte(destination) == value
    assert cpu.p == flags
    assert cpu.pc == 0x0569
    assert cpu.cycles == 4


@pytest.mark.parametrize("opcode, register", [
    (0xA5, "a"),  # LDA zero page
    (0xA6, "x"),  # LDX zero page
    (0xA4, "y"),  # LDY zero page
])
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


@pytest.mark.parametrize("opcode, register, index_register", [
    (0xB5, "a", "x"),  # LDA zero page,X
    (0xB6, "x", "y"),  # LDX zero page,Y
    (0xB4, "y", "x"),  # LDY zero page,X
])
@pytest.mark.parametrize("operand, index, source", [(0x20, 0x04, 0x24), (0xF0, 0x20, 0x10)])
@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
def test_indexed_zero_page_loads(make_cpu, opcode, register, index_register, operand, index, source, value):
    # Put the data away from the instruction and start N/Z opposite to the expected values.
    cpu, machine = make_cpu(start_address=0x0567)
    setattr(cpu, register, 0x55)
    setattr(cpu, index_register, index)
    cpu.negative = not bool(value & 0x80)
    cpu.zero = value != 0
    machine.write_byte(0x0567, opcode)
    machine.write_byte(0x0568, operand)
    machine.write_byte(source, value)

    # The indexed address supplies the register and its N/Z flags.
    cpu.step()
    assert getattr(cpu, register) == value
    assert cpu.negative is bool(value & 0x80)
    assert cpu.zero is (value == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 4


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
    machine.write_byte(0x0567, 0x81)  # STA opcode
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
    machine.write_byte(0x0567, 0x91)  # STA opcode
    machine.write_byte(0x0568, pointer_low)
    machine.write_byte(pointer_low, low)
    machine.write_byte(pointer_high, high)
    machine.write_byte(destination, value ^ 0xFF)

    # The effective address receives the byte, regardless of page crossing.
    cpu.step()
    assert machine.read_byte(destination) == value
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("operand, index, pointer_low, pointer_high", [
    (0x20, 0x04, 0x24, 0x25),
    (0xF0, 0x20, 0x10, 0x11),
    (0xFC, 0x03, 0xFF, 0x00),
])
@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
def test_lda_indexed_indirect_loads_accumulator(make_cpu, operand, index, pointer_low, pointer_high, value):
    # Place the instruction, indexed pointer, and source byte at separate addresses.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = 0x55
    cpu.x = index
    cpu.negative = not bool(value & 0x80)
    cpu.zero = value != 0
    machine.write_byte(0x0567, 0xA1)  # LDA opcode
    machine.write_byte(0x0568, operand)
    machine.write_byte(pointer_low, 0x45)
    machine.write_byte(pointer_high, 0x03)
    machine.write_byte(0x0345, value)

    # The selected byte determines A, N, and Z for each pointer wrap case.
    cpu.step()
    assert cpu.a == value
    assert cpu.negative is bool(value & 0x80)
    assert cpu.zero is (value == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("pointer_low, pointer_high, low, high, index, source, cycles", [
    (0x20, 0x21, 0x30, 0x12, 0x04, 0x1234, 5),
    (0xFF, 0x00, 0xFF, 0x12, 0x01, 0x1300, 6),
    (0x20, 0x21, 0xFF, 0xFF, 0x01, 0x0000, 6),
])
@pytest.mark.parametrize("value", [0x00, 0x7F, 0x80, 0xFF])
def test_lda_indirect_indexed_loads_accumulator(
    make_cpu, pointer_low, pointer_high, low, high, index, source, cycles, value,
):
    # A zero-page pointer supplies the base address before indexing with Y.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = 0x55
    cpu.y = index
    cpu.negative = not bool(value & 0x80)
    cpu.zero = value != 0
    machine.write_byte(0x0567, 0xB1)  # LDA opcode
    machine.write_byte(0x0568, pointer_low)
    machine.write_byte(pointer_low, low)
    machine.write_byte(pointer_high, high)
    machine.write_byte(source, value)

    # The selected byte determines A and N/Z, with an extra cycle on page crossing.
    cpu.step()
    assert cpu.a == value
    assert cpu.negative is bool(value & 0x80)
    assert cpu.zero is (value == 0)
    assert cpu.pc == 0x0569
    assert cpu.cycles == cycles


@pytest.mark.parametrize("opcode, index_register", [
    (0x9D, "x"),  # STA absolute,X
    (0x99, "y"),  # STA absolute,Y
])
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
    (0xBD, "a", "x"),  # LDA absolute,X
    (0xB9, "a", "y"),  # LDA absolute,Y
    (0xBE, "x", "y"),  # LDX absolute,Y
    (0xBC, "y", "x"),  # LDY absolute,X
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


@pytest.mark.parametrize("opcode, register", [
    (0xAD, "a"),  # LDA absolute
    (0xAE, "x"),  # LDX absolute
    (0xAC, "y"),  # LDY absolute
])
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


@pytest.mark.parametrize("opcode, register", [
    (0x8D, "a"),  # STA absolute
    (0x8E, "x"),  # STX absolute
    (0x8C, "y"),  # STY absolute
])
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


@pytest.mark.parametrize("opcode, register", [
    (0x8D, "a"),  # STA absolute
    (0x8E, "x"),  # STX absolute
    (0x8C, "y"),  # STY absolute
])
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
    machine.write_byte(0x0000, 0xBA)  # TSX opcode

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
    machine.write_byte(0x0000, 0x9A)  # TXS opcode

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
    [
        (0x8A, "x", "a"),  # TXA
        (0x98, "y", "a"),  # TYA
        (0xAA, "a", "x"),  # TAX
        (0xA8, "a", "y"),  # TAY
    ],
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
        (0xF0, "zero", True),       # BEQ
        (0xD0, "zero", False),      # BNE
        (0x10, "negative", False),  # BPL
        (0x30, "negative", True),   # BMI
        (0x90, "carry", False),     # BCC
        (0xB0, "carry", True),      # BCS
        (0x50, "overflow", False),  # BVC
        (0x70, "overflow", True),   # BVS
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
    machine.write_byte(0x0000, 0x18)  # CLC opcode
    machine.write_byte(0x0001, 0x38)  # SEC opcode
    machine.write_byte(0x0002, 0x58)  # CLI opcode
    machine.write_byte(0x0003, 0x78)  # SEI opcode
    machine.write_byte(0x0004, 0xD8)  # CLD opcode
    machine.write_byte(0x0005, 0xF8)  # SED opcode
    machine.write_byte(0x0006, 0xB8)  # CLV opcode
    machine.write_byte(0x0007, 0xEA)  # NOP opcode

    # Each step contributes two, yielding sixteen cycles in total.
    for expected_cycles in range(2, 17, 2):
        cpu.step()
        assert cpu.cycles == expected_cycles


def test_cycles_do_not_wrap_at_16_bits(make_cpu):
    # Reuse one RAM NOP to advance the cumulative counter past $FFFF.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xEA)  # NOP opcode
    for _ in range(32769):
        cpu.pc = 0x0000
        cpu.step()

    # The Python integer is not limited to a 16-bit CPU register width.
    assert cpu.cycles == 65538


def test_cycles_are_read_only_and_preserved_by_reset(make_cpu):
    # A new CPU starts at zero and counts a completed instruction.
    cpu, machine = make_cpu()
    machine.write_byte(0x0000, 0xEA)  # NOP opcode
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
    machine.write_byte(0x0000, 0xEA)  # NOP opcode
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
    machine.write_byte(0x0234, 0x78)  # SEI opcode
    machine.write_byte(0x0235, 0xD8)  # CLD opcode
    machine.write_byte(0x0236, 0x02)  # Unsupported opcode
    machine.write_byte(0x0237, 0x42)
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


@pytest.mark.parametrize("initial, value, incoming_carry, expected, carry, overflow", [
    (0x7F, 0x00, True, 0x80, False, True),
    (0xFF, 0x00, True, 0x00, True, False),
    (0x01, 0x01, False, 0x02, False, False),
    (0x80, 0x80, False, 0x00, True, True),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("operand, index, pointer", [
    (0x20, 0x04, 0x24),
    (0xF0, 0x20, 0x10),
    (0xFC, 0x03, 0xFF),
])
def test_adc_indexed_indirect(
    make_cpu, initial, value, incoming_carry, expected, carry, overflow, decimal, operand, index, pointer,
):
    # Set X and the arithmetic flags before following the indexed zero-page pointer.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.x = index
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0x61)  # ADC (zp,X) opcode
    machine.write_byte(0x0568, operand)
    machine.write_byte(pointer, 0x34)
    machine.write_byte((pointer + 1) & 0xFF, 0x02)
    machine.write_byte(0x0234, value)

    # Binary addition updates A and C/V/N/Z independently of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("initial, value, incoming_carry, expected, carry, overflow", [
    (0x7F, 0x00, True, 0x80, False, True),
    (0xFF, 0x00, True, 0x00, True, False),
    (0x01, 0x01, False, 0x02, False, False),
    (0x80, 0x80, False, 0x00, True, True),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("operand, low, high, index, source, cycles", [
    (0x20, 0x30, 0x02, 0x04, 0x0234, 5),
    (0xFF, 0xFF, 0x02, 0x01, 0x0300, 6),
])
def test_adc_indirect_indexed(
    make_cpu, initial, value, incoming_carry, expected, carry, overflow, decimal, operand, low, high, index, source,
    cycles,
):
    # Set Y and the arithmetic flags before following the zero-page pointer.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.y = index
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0x71)  # ADC (zp),Y opcode
    machine.write_byte(0x0568, operand)
    machine.write_byte(operand, low)
    machine.write_byte((operand + 1) & 0xFF, high)
    machine.write_byte(source, value)

    # Binary addition updates A and C/V/N/Z independently of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == cycles


def test_adc_indirect_indexed_wraps_effective_address(make_cpu):
    # The wrapped target shares $0000 with the pointer's high byte, so both must contain $FF.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = 0x00
    cpu.y = 0x01
    cpu.carry = False
    cpu.decimal = True
    machine.write_byte(0x0567, 0x71)  # ADC (zp),Y opcode
    machine.write_byte(0x0568, 0xFF)
    machine.write_byte(0x00FF, 0xFF)
    machine.write_byte(0x0000, 0xFF)

    # The $FFFF + Y address wraps to $0000 and still takes the crossing cycle.
    cpu.step()
    assert cpu.a == 0xFF
    assert cpu.carry is False
    assert cpu.overflow is False
    assert cpu.negative is True
    assert cpu.zero is False
    assert cpu.decimal is True
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("initial, value, incoming_carry, expected, carry, overflow", [
    (0x80, 0x01, True, 0x7F, True, True),
    (0x00, 0x00, False, 0xFF, False, False),
    (0x42, 0x42, True, 0x00, True, False),
    (0x7F, 0xFF, True, 0x80, False, True),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("operand, index, pointer", [
    (0x20, 0x04, 0x24),
    (0xF0, 0x20, 0x10),
    (0xFC, 0x03, 0xFF),
])
def test_sbc_indexed_indirect(
    make_cpu, initial, value, incoming_carry, expected, carry, overflow, decimal, operand, index, pointer,
):
    # Set X and the arithmetic flags before following the indexed zero-page pointer.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.x = index
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0xE1)  # SBC (zp,X) opcode
    machine.write_byte(0x0568, operand)
    machine.write_byte(pointer, 0x34)
    machine.write_byte((pointer + 1) & 0xFF, 0x02)
    machine.write_byte(0x0234, value)

    # Binary subtraction updates A and C/V/N/Z independently of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("initial, value, incoming_carry, expected, carry, overflow", [
    (0x80, 0x01, True, 0x7F, True, True),
    (0x00, 0x00, False, 0xFF, False, False),
    (0x42, 0x42, True, 0x00, True, False),
    (0x7F, 0xFF, True, 0x80, False, True),
])
@pytest.mark.parametrize("decimal", [False, True])
@pytest.mark.parametrize("operand, low, high, index, source, cycles", [
    (0x20, 0x30, 0x02, 0x04, 0x0234, 5),
    (0xFF, 0xFF, 0x02, 0x01, 0x0300, 6),
])
def test_sbc_indirect_indexed(
    make_cpu, initial, value, incoming_carry, expected, carry, overflow, decimal, operand, low, high, index, source,
    cycles,
):
    # Set Y and the arithmetic flags before following the zero-page pointer.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = initial
    cpu.y = index
    cpu.carry = incoming_carry
    cpu.decimal = decimal
    cpu.overflow = not overflow
    cpu.negative = not bool(expected & 0x80)
    cpu.zero = expected != 0
    machine.write_byte(0x0567, 0xF1)  # SBC (zp),Y opcode
    machine.write_byte(0x0568, operand)
    machine.write_byte(operand, low)
    machine.write_byte((operand + 1) & 0xFF, high)
    machine.write_byte(source, value)

    # Binary subtraction updates A and C/V/N/Z independently of D.
    cpu.step()
    assert cpu.a == expected
    assert cpu.carry is carry
    assert cpu.overflow is overflow
    assert cpu.negative is bool(expected & 0x80)
    assert cpu.zero is (expected == 0)
    assert cpu.decimal is decimal
    assert cpu.pc == 0x0569
    assert cpu.cycles == cycles


def test_sbc_indirect_indexed_wraps_effective_address(make_cpu):
    # The wrapped target shares $0000 with the pointer's high byte, so both must contain $FF.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = 0x00
    cpu.y = 0x01
    cpu.carry = True
    machine.write_byte(0x0567, 0xF1)  # SBC (zp),Y opcode
    machine.write_byte(0x0568, 0xFF)
    machine.write_byte(0x00FF, 0xFF)
    machine.write_byte(0x0000, 0xFF)

    # The $FFFF + Y address wraps to $0000 and still takes the crossing cycle.
    cpu.step()
    assert cpu.a == 0x01
    assert cpu.carry is False
    assert cpu.overflow is False
    assert cpu.negative is False
    assert cpu.zero is False
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("value, compared, carry, zero, negative", [
    (0x40, 0x41, False, False, True),
    (0x40, 0x40, True, True, False),
    (0x40, 0x3F, True, False, False),
    (0x00, 0x80, False, False, True),
])
@pytest.mark.parametrize("operand, index, pointer", [
    (0x20, 0x04, 0x24),
    (0xF0, 0x20, 0x10),
    (0xFC, 0x03, 0xFF),
])
def test_cmp_indexed_indirect_updates_cnz(
    make_cpu, value, compared, carry, zero, negative, operand, index, pointer,
):
    # Set X and opposite C/Z/N values before following the indexed zero-page pointer.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = value
    cpu.x = index
    cpu.carry = not carry
    cpu.zero = not zero
    cpu.negative = not negative
    machine.write_byte(0x0567, 0xC1)  # CMP (zp,X) opcode
    machine.write_byte(0x0568, operand)
    machine.write_byte(pointer, 0x34)
    machine.write_byte((pointer + 1) & 0xFF, 0x02)
    machine.write_byte(0x0234, compared)

    # CMP updates C/Z/N from the difference without storing it in A.
    cpu.step()
    assert cpu.a == value
    assert cpu.carry is carry
    assert cpu.zero is zero
    assert cpu.negative is negative
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("value, compared, carry, zero, negative", [
    (0x40, 0x41, False, False, True),
    (0x40, 0x40, True, True, False),
    (0x40, 0x3F, True, False, False),
    (0x00, 0x80, False, False, True),
])
@pytest.mark.parametrize("operand, low, high, index, source, cycles", [
    (0x20, 0x30, 0x02, 0x04, 0x0234, 5),
    (0xFF, 0xFF, 0x02, 0x01, 0x0300, 6),
])
def test_cmp_indirect_indexed_updates_cnz(
    make_cpu, value, compared, carry, zero, negative, operand, low, high, index, source, cycles,
):
    # Set Y and opposite C/Z/N values before following the zero-page pointer.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = value
    cpu.y = index
    cpu.carry = not carry
    cpu.zero = not zero
    cpu.negative = not negative
    machine.write_byte(0x0567, 0xD1)  # CMP (zp),Y opcode
    machine.write_byte(0x0568, operand)
    machine.write_byte(operand, low)
    machine.write_byte((operand + 1) & 0xFF, high)
    machine.write_byte(source, compared)

    # CMP updates C/Z/N from the difference without storing it in A.
    cpu.step()
    assert cpu.a == value
    assert cpu.carry is carry
    assert cpu.zero is zero
    assert cpu.negative is negative
    assert cpu.pc == 0x0569
    assert cpu.cycles == cycles


def test_cmp_indirect_indexed_updates_cnz_wraps_effective_address(make_cpu):
    # The wrapped target shares $0000 with the pointer's high byte, so both must contain $FF.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = 0x7F
    cpu.y = 0x01
    machine.write_byte(0x0567, 0xD1)  # CMP (zp),Y opcode
    machine.write_byte(0x0568, 0xFF)
    machine.write_byte(0x00FF, 0xFF)
    machine.write_byte(0x0000, 0xFF)

    # The $FFFF + Y address wraps to $0000 and still takes the crossing cycle.
    cpu.step()
    assert cpu.a == 0x7F
    assert cpu.carry is False
    assert cpu.zero is False
    assert cpu.negative is True
    assert cpu.pc == 0x0569
    assert cpu.cycles == 6


@pytest.mark.parametrize("value, initial_sp, stack_address, final_sp", [
    (0x80, 0xFD, 0x01FD, 0xFC),
    (0x00, 0x00, 0x0100, 0xFF),
])
@pytest.mark.parametrize("status", [0x20, 0xFF])
def test_pha_pushes_accumulator(make_cpu, value, initial_sp, stack_address, final_sp, status):
    # Seed the destination and all status fields so the push and preservation are observable.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = value
    cpu.sp = initial_sp
    cpu.p = status
    machine.write_byte(0x0567, 0x48)  # PHA opcode
    machine.write_byte(stack_address, value ^ 0xFF)

    # PHA writes at the pre-decrement stack position and preserves A and P.
    cpu.step()
    assert machine.read_byte(stack_address) == value
    assert cpu.a == value
    assert cpu.p == status
    assert cpu.sp == final_sp
    assert cpu.pc == 0x0568
    assert cpu.cycles == 3


@pytest.mark.parametrize("initial_sp, stack_address, value, final_sp, negative, zero", [
    (0xFC, 0x01FD, 0x80, 0xFD, True, False),
    (0xFF, 0x0100, 0x00, 0x00, False, True),
])
def test_pla_pulls_accumulator_and_updates_nz(
    make_cpu, initial_sp, stack_address, value, final_sp, negative, zero,
):
    # Seed the stack through Machine and start N/Z opposite to the pulled value.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.a = value ^ 0xFF
    cpu.sp = initial_sp
    cpu.negative = not negative
    cpu.zero = not zero
    machine.write_byte(0x0567, 0x68)  # PLA opcode
    machine.write_byte(stack_address, value)

    # PLA pre-increments SP, loads A, and updates N/Z from the pulled byte.
    cpu.step()
    assert cpu.a == value
    assert cpu.negative is negative
    assert cpu.zero is zero
    assert cpu.sp == final_sp
    assert cpu.pc == 0x0568
    assert cpu.cycles == 4


@pytest.mark.parametrize("software_break, status", [(False, 0xA5), (True, 0xB5)])
@pytest.mark.parametrize("initial_sp, stack_address, final_sp", [
    (0xFD, 0x01FD, 0xFC),
    (0x00, 0x0100, 0xFF),
])
def test_php_pushes_status(make_cpu, software_break, status, initial_sp, stack_address, final_sp):
    # Seed software B, the other status fields, and a distinct stack destination.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.p = status
    cpu.sp = initial_sp
    machine.write_byte(0x0567, 0x08)  # PHP opcode
    machine.write_byte(stack_address, 0x00)

    # The saved B and reserved bits are forced high without changing software B.
    cpu.step()
    assert machine.read_byte(stack_address) == (status | 0x30)
    assert cpu.p == status
    assert cpu.break_flag is software_break
    assert cpu.sp == final_sp
    assert cpu.pc == 0x0568
    assert cpu.cycles == 3


@pytest.mark.parametrize(
    "status, software_break, initial_sp, stack_address, final_sp, expected_flags, expected_p",
    [
        (0xBA, False, 0xFF, 0x0100, 0x00, (True, False, True, False, True, False), 0xAA),
        (0xCF, True, 0xFC, 0x01FD, 0xFD, (True, True, True, True, True, True), 0xFF),
        (0x30, False, 0xFE, 0x01FF, 0xFF, (False, False, False, False, False, False), 0x20),
    ],
)
def test_plp_restores_status(
    make_cpu, status, software_break, initial_sp, stack_address, final_sp, expected_flags, expected_p,
):
    # Set all six hardware flags opposite to their expected values and seed the stack directly.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.sp = initial_sp
    cpu.break_flag = software_break
    cpu.negative, cpu.overflow, cpu.decimal, cpu.interrupt_disable, cpu.zero, cpu.carry = (
        not flag for flag in expected_flags
    )
    machine.write_byte(0x0567, 0x28)  # PLP opcode
    machine.write_byte(stack_address, status)

    # PLP restores hardware flags while preserving software B and wrapping SP within page 1.
    cpu.step()
    actual_flags = (
        cpu.negative, cpu.overflow, cpu.decimal, cpu.interrupt_disable, cpu.zero, cpu.carry,
    )
    assert actual_flags == expected_flags
    assert cpu.p == expected_p
    assert cpu.break_flag is software_break
    assert cpu.sp == final_sp
    assert cpu.pc == 0x0568
    assert cpu.cycles == 4


def test_brk_pushes_interrupt_frame_and_loads_vector(make_cpu):
    # Start with I clear and SP at zero so one case covers a normal PC and stack wrap.
    cpu, machine = make_cpu(start_address=0x0234)
    cpu.sp = 0x00
    cpu.p = 0x29
    machine.write_byte(0x0234, 0x00)  # BRK opcode

    # BRK saves PC+2 and pre-I status high-to-low, then follows the default zero IRQ vector.
    cpu.step()
    assert machine.read_byte(0x0100) == 0x02
    assert machine.read_byte(0x01FF) == 0x36
    assert machine.read_byte(0x01FE) == 0x39
    assert cpu.sp == 0xFD
    assert cpu.pc == 0x0000
    assert cpu.p == 0x2D
    assert cpu.interrupt_disable is True
    assert cpu.cycles == 7


@pytest.mark.parametrize("interrupt_disable, software_break", [(False, False), (True, True)])
def test_nmi_entry_and_rti_restore_interrupted_state(make_cpu, monkeypatch, interrupt_disable, software_break):
    # Install an RTI handler in RAM and supply an NMI vector with observable read order.
    cpu, machine = make_cpu(start_address=0x0234)
    cpu.sp = 0x00
    cpu.p = 0xC9 | (interrupt_disable << 2) | (software_break << 4)
    initial_status = cpu.p
    machine.write_byte(0x0456, 0x40)  # RTI opcode
    reads = []
    original_read = machine.read_byte

    def read_byte(address):
        reads.append(address)
        if address == 0xFFFA:
            return 0x56
        if address == 0xFFFB:
            return 0x04
        return original_read(address)

    monkeypatch.setattr(machine, "read_byte", read_byte)

    # Entry saves the exact next PC and pre-entry flags, wrapping within the stack page.
    cpu.enter_nmi()
    assert reads == [0xFFFA, 0xFFFB]
    assert machine.read_byte(0x0100) == 0x02
    assert machine.read_byte(0x01FF) == 0x34
    assert machine.read_byte(0x01FE) == (initial_status & 0xEF)
    assert cpu.sp == 0xFD
    assert cpu.pc == 0x0456
    assert cpu.interrupt_disable is True
    assert cpu.break_flag is software_break
    assert cpu.cycles == 7

    # RTI restores the saved hardware flags and resumes at the interrupted instruction.
    cpu.step()
    assert cpu.pc == 0x0234
    assert cpu.sp == 0x00
    assert cpu.p == initial_status
    assert cpu.cycles == 13


def test_rti_restores_status_and_program_counter(make_cpu):
    # Seed an ordinary RTI frame through Machine with all hardware flags opposite to their saved values.
    cpu, machine = make_cpu(start_address=0x0567)
    cpu.sp = 0xFC
    cpu.break_flag = False
    expected_flags = (False, False, True, False, False, True)
    cpu.negative, cpu.overflow, cpu.decimal, cpu.interrupt_disable, cpu.zero, cpu.carry = (
        not flag for flag in expected_flags
    )
    machine.write_byte(0x0567, 0x40)  # RTI opcode
    machine.write_byte(0x01FD, 0x29)  # Status
    machine.write_byte(0x01FE, 0x34)  # Return PC low
    machine.write_byte(0x01FF, 0xC2)  # Return PC high

    # RTI pulls status, PC low, then PC high and preserves the software B field.
    cpu.step()
    actual_flags = (
        cpu.negative, cpu.overflow, cpu.decimal, cpu.interrupt_disable, cpu.zero, cpu.carry,
    )
    assert actual_flags == expected_flags
    assert cpu.p == 0x29
    assert cpu.break_flag is False
    assert cpu.sp == 0xFF
    assert cpu.pc == 0xC234
    assert cpu.cycles == 6
