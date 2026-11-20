"""Model NES CPU registers, functional startup, and single-instruction execution."""

import logging


logger = logging.getLogger("cpu")


class CPU:
    """CPU state with byte registers A/X/Y/SP and a 16-bit program counter.

    Register setters assert their value ranges; callers supply boolean flag values. Construction
    clears register storage once, then resets through the connected Machine without executing an instruction.
    B is software inspection state rather than a physical processor latch.
    """

    def __init__(self, machine):
        # CPU memory accesses use Machine's address routing.
        self._machine = machine

        # Clear state only at construction; reset applies its effects to these initial values.
        self._a = 0
        self._x = 0
        self._y = 0
        self._sp = 0
        self._pc = 0
        self._cycles = 0
        self._carry = False
        self._zero = False
        self._interrupt_disable = False
        self._decimal = False
        self._break_flag = False
        self._overflow = False
        self._negative = False

        # Starting SP at zero makes the first reset's three decrements produce $FD.
        self.reset()


    def reset(self):
        # Functional reset changes SP and I without the hardware's dummy stack reads.
        self._sp = (self._sp - 3) & 0xFF
        self._interrupt_disable = True

        # The reset vector is little-endian; loading PC does not fetch an opcode at its target.
        low = self._machine.read_byte(0xFFFC)
        high = self._machine.read_byte(0xFFFD)
        self._pc = low | (high << 8)

        # Report the state only after reset has completed.
        self.log_state("Reset completed")


    def step(self):
        """Execute one instruction at the current program counter."""
        # Save the instruction address before consuming the opcode.
        address = self._pc
        opcode = self._fetch_byte()

        # Leave an unsupported opcode at PC so the caller can inspect or retry it.
        handler = self._instruction_handlers[opcode]
        if handler is None:
            self._pc = address
            raise NotImplementedError(f"CPU opcode 0x{opcode:02X} at address 0x{address:04X} is not implemented")
        handler(self, address, opcode)


    def _fetch_byte(self):
        """Read the byte at PC and advance the 16-bit PC by one."""
        address = self._pc
        value = self._machine.read_byte(address)
        self._pc = (address + 1) & 0xFFFF
        return value


    def _fetch_word(self):
        """Read a little-endian word at PC and advance the 16-bit PC by two."""
        # Fetch the low byte first and wrap the bus address after $FFFF.
        address = self._pc
        low = self._machine.read_byte(address)
        high = self._machine.read_byte((address + 1) & 0xFFFF)

        # Consume the word after both reads succeed.
        self._pc = (address + 2) & 0xFFFF
        return low | (high << 8)


    def log_instruction(self, address, instruction_bytes, mnemonic, operands=""):
        """Log supplied instruction metadata and the current CPU state."""
        # Skip all trace formatting when the effective logger level disables DEBUG.
        if not logger.isEnabledFor(logging.DEBUG):
            return

        # Align fetched bytes and decoded text without accessing emulated memory.
        byte_text = " ".join(f"{byte:02X}" for byte in instruction_bytes)
        prefix = f"{address:04X}   {byte_text:<8}   {mnemonic:<3} {operands:<20}"

        # The shared state logger appends registers and cycles at column 44.
        self.log_state(prefix, separator=" ")


    def log_state(self, event, separator=": "):
        """Log an event with the current registers and symbolic status flags at DEBUG level."""
        # Display status from N to C, with the constant bit 5 shown as 1.
        p = self.p
        flags = "".join(name if p & (0x80 >> bit) else "-" for bit, name in enumerate("NV1BDIZC"))

        # Treat the event text as data and append a snapshot of the current registers.
        logger.debug(
            "%s%sA=%02X X=%02X Y=%02X SP=%02X PC=%04X P=%s CYC=%d",
            event, separator, self._a, self._x, self._y, self._sp, self._pc, flags, self._cycles,
        )


    @property
    def cycles(self):
        """Return the total nominal cycles of completed instructions."""
        return self._cycles


    @property
    def a(self):
        return self._a


    @a.setter
    def a(self, value):
        assert 0 <= value <= 0xFF
        self._a = value


    @property
    def x(self):
        return self._x


    @x.setter
    def x(self, value):
        assert 0 <= value <= 0xFF
        self._x = value


    @property
    def y(self):
        return self._y


    @y.setter
    def y(self, value):
        assert 0 <= value <= 0xFF
        self._y = value


    @property
    def sp(self):
        return self._sp


    @sp.setter
    def sp(self, value):
        assert 0 <= value <= 0xFF
        self._sp = value


    @property
    def pc(self):
        return self._pc


    @pc.setter
    def pc(self, value):
        assert 0 <= value <= 0xFFFF
        self._pc = value


    @property
    def carry(self):
        return self._carry


    @carry.setter
    def carry(self, value):
        self._carry = value


    @property
    def zero(self):
        return self._zero


    @zero.setter
    def zero(self, value):
        self._zero = value


    @property
    def interrupt_disable(self):
        return self._interrupt_disable


    @interrupt_disable.setter
    def interrupt_disable(self, value):
        self._interrupt_disable = value


    @property
    def decimal(self):
        return self._decimal


    @decimal.setter
    def decimal(self, value):
        self._decimal = value


    @property
    def break_flag(self):
        return self._break_flag


    @break_flag.setter
    def break_flag(self, value):
        self._break_flag = value


    @property
    def overflow(self):
        return self._overflow


    @overflow.setter
    def overflow(self, value):
        self._overflow = value


    @property
    def negative(self):
        return self._negative


    @negative.setter
    def negative(self, value):
        self._negative = value


    @property
    def p(self):
        # Bit 5 is constant; bit 4 reflects the software B field.
        return (
            (self._negative << 7)
            | (self._overflow << 6)
            | 0x20
            | (self._break_flag << 4)
            | (self._decimal << 3)
            | (self._interrupt_disable << 2)
            | (self._zero << 1)
            | self._carry
        )


    @p.setter
    def p(self, value):
        # Check the complete byte before replacing any individual status field.
        assert 0 <= value <= 0xFF

        # Replace all seven status fields; input bit 5 has no stored counterpart.
        self._carry = bool(value & 0x01)
        self._zero = bool(value & 0x02)
        self._interrupt_disable = bool(value & 0x04)
        self._decimal = bool(value & 0x08)
        self._break_flag = bool(value & 0x10)
        self._overflow = bool(value & 0x40)
        self._negative = bool(value & 0x80)


    def _jsr_absolute(self, address, opcode):
        # Fetch the low operand before pushing the address of the high operand.
        low = self._fetch_byte()
        self._machine.write_byte(0x0100 | self._sp, self._pc >> 8)
        self._sp = (self._sp - 1) & 0xFF
        self._machine.write_byte(0x0100 | self._sp, self._pc & 0xFF)
        self._sp = (self._sp - 1) & 0xFF

        # Fetch the high operand after the writes, which may have changed it in RAM.
        high = self._fetch_byte()
        self._pc = low | (high << 8)
        self._cycles += 6
        self.log_instruction(address, (opcode, low, high), "JSR", f"${self._pc:04X}")


    def _rts(self, address, opcode):
        # Pull the low byte first, wrapping SP within the stack page.
        self._sp = (self._sp + 1) & 0xFF
        low = self._machine.read_byte(0x0100 | self._sp)
        self._sp = (self._sp + 1) & 0xFF
        high = self._machine.read_byte(0x0100 | self._sp)

        # Resume after the saved address and report the completed instruction.
        self._pc = ((high << 8 | low) + 1) & 0xFFFF
        self._cycles += 6
        self.log_instruction(address, (opcode,), "RTS")


    def _jmp_absolute(self, address, opcode):
        # The operand itself is the destination, not a pointer to another address.
        destination = self._fetch_word()
        self._pc = destination

        # Absolute JMP takes three cycles and traces the already fetched bytes.
        self._cycles += 3
        self.log_instruction(address, (opcode, destination & 0xFF, destination >> 8), "JMP", f"${destination:04X}")


    def _jmp_indirect(self, address, opcode):
        # The original CPU wraps the pointer's high-byte read within its page.
        pointer = self._fetch_word()
        low = self._machine.read_byte(pointer)
        high_address = (pointer & 0xFF00) | ((pointer + 1) & 0xFF)
        high = self._machine.read_byte(high_address)
        self._pc = low | (high << 8)

        # The trace identifies the operand using the bytes already fetched.
        self._cycles += 5
        self.log_instruction(address, (opcode, pointer & 0xFF, pointer >> 8), "JMP", f"(${pointer:04X})")


    def _lda_indexed_indirect(self, address, opcode):
        # X selects a wrapping zero-page pointer to the source byte.
        operand = self._fetch_byte()
        pointer = (operand + self._x) & 0xFF
        source = self._read_zero_page_word(pointer)
        self._a = self._machine.read_byte(source)

        # Set N/Z and trace the completed instruction without the discarded read.
        self._negative = bool(self._a & 0x80)
        self._zero = self._a == 0
        self._cycles += 6
        self.log_instruction(address, (opcode, operand), "LDA", f"(${operand:02X},X)")


    def _lda_indirect_indexed(self, address, opcode):
        # Y indexes the address stored in a wrapping zero-page pointer.
        operand = self._fetch_byte()
        base = self._read_zero_page_word(operand)
        source = (base + self._y) & 0xFFFF
        self._a = self._machine.read_byte(source)

        # Count the page-crossing cost without the provisional hardware read.
        self._negative = bool(self._a & 0x80)
        self._zero = self._a == 0
        self._cycles += 5 + (base >> 8 != source >> 8)
        self.log_instruction(address, (opcode, operand), "LDA", f"(${operand:02X}),Y")


    def _lda_zero_page(self, address, opcode):
        destination = self._fetch_byte()
        self._a = self._machine.read_byte(destination)
        self._finish_zero_page_update(address, opcode, "LDA", destination, self._a)


    def _ldx_zero_page(self, address, opcode):
        destination = self._fetch_byte()
        self._x = self._machine.read_byte(destination)
        self._finish_zero_page_update(address, opcode, "LDX", destination, self._x)


    def _ldy_zero_page(self, address, opcode):
        destination = self._fetch_byte()
        self._y = self._machine.read_byte(destination)
        self._finish_zero_page_update(address, opcode, "LDY", destination, self._y)


    def _lda_zero_page_x(self, address, opcode):
        operand, self._a = self._read_indexed_zero_page(self._x)
        self._finish_indexed_zero_page_load(address, opcode, operand, self._a, "LDA", "X")


    def _ldx_zero_page_y(self, address, opcode):
        operand, self._x = self._read_indexed_zero_page(self._y)
        self._finish_indexed_zero_page_load(address, opcode, operand, self._x, "LDX", "Y")


    def _ldy_zero_page_x(self, address, opcode):
        operand, self._y = self._read_indexed_zero_page(self._x)
        self._finish_indexed_zero_page_load(address, opcode, operand, self._y, "LDY", "X")


    def _read_indexed_zero_page(self, index):
        # The index wraps within zero page; the discarded hardware read is omitted.
        operand = self._fetch_byte()
        value = self._machine.read_byte((operand + index) & 0xFF)
        return operand, value


    def _finish_indexed_zero_page_load(self, address, opcode, operand, value, mnemonic, index_name):
        # N and Z describe the loaded byte.
        self._negative = bool(value & 0x80)
        self._zero = value == 0

        # Trace the already fetched operand after updating the destination register.
        self._cycles += 4
        self.log_instruction(address, (opcode, operand), mnemonic, f"${operand:02X},{index_name}")


    def _finish_zero_page_update(self, address, opcode, mnemonic, destination, value):
        # N and Z reflect the resulting register byte.
        self._negative = bool(value & 0x80)
        self._zero = value == 0

        # The trace uses the operand already fetched through Machine.
        self._cycles += 3
        self.log_instruction(address, (opcode, destination), mnemonic, f"${destination:02X}")


    def _cmp_immediate(self, address, opcode):
        self._compare_immediate(address, opcode, "CMP", self._a)


    def _cpx_immediate(self, address, opcode):
        self._compare_immediate(address, opcode, "CPX", self._x)


    def _cpy_immediate(self, address, opcode):
        self._compare_immediate(address, opcode, "CPY", self._y)


    def _compare_immediate(self, address, opcode, mnemonic, value):
        # Compare the register with the fetched immediate byte.
        operand = self._fetch_byte()
        self._compare(value, operand)

        # The fetched operand is reused for the trace.
        self._cycles += 2
        self.log_instruction(address, (opcode, operand), mnemonic, f"#${operand:02X}")


    def _compare(self, value, operand):
        # C uses an unsigned comparison; N and Z use the eight-bit difference.
        difference = (value - operand) & 0xFF
        self._carry = value >= operand
        self._zero = difference == 0
        self._negative = bool(difference & 0x80)


    def _cmp_absolute(self, address, opcode):
        self._compare_absolute(address, opcode, "CMP", self._a)


    def _cpx_absolute(self, address, opcode):
        self._compare_absolute(address, opcode, "CPX", self._x)


    def _cpy_absolute(self, address, opcode):
        self._compare_absolute(address, opcode, "CPY", self._y)


    def _cmp_absolute_x(self, address, opcode):
        self._compare_absolute_indexed(address, opcode, self._x, "X")


    def _cmp_absolute_y(self, address, opcode):
        self._compare_absolute_indexed(address, opcode, self._y, "Y")


    def _compare_absolute_indexed(self, address, opcode, index, index_name):
        # Compare A with the indexed byte using the existing functional read model.
        base, operand, crossed = self._read_absolute_indexed(index)
        self._compare(self._a, operand)

        # Account for page crossing and trace the fetched base address.
        self._cycles += 4 + crossed
        self.log_instruction(address, (opcode, base & 0xFF, base >> 8), "CMP", f"${base:04X},{index_name}")


    def _compare_absolute(self, address, opcode, mnemonic, value):
        # Compare against the byte selected by the little-endian address.
        destination = self._fetch_word()
        operand = self._machine.read_byte(destination)
        self._compare(value, operand)

        # Reuse the fetched address for the trace.
        self._cycles += 4
        self.log_instruction(address, (opcode, destination & 0xFF, destination >> 8), mnemonic, f"${destination:04X}")


    def _adc_immediate(self, address, opcode):
        operand = self._fetch_byte()
        self._add_with_carry(operand)
        self._finish_immediate_update(address, opcode, "ADC", operand, self._a)


    def _adc_zero_page(self, address, opcode):
        destination = self._fetch_byte()
        operand = self._machine.read_byte(destination)
        self._add_with_carry(operand)
        self._finish_zero_page_update(address, opcode, "ADC", destination, self._a)


    def _adc_absolute(self, address, opcode):
        destination = self._fetch_word()
        operand = self._machine.read_byte(destination)
        self._add_with_carry(operand)
        self._finish_absolute_update(address, opcode, "ADC", destination, self._a)


    def _adc_absolute_x(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._x)
        self._add_with_carry(operand)
        self._finish_indexed_update(address, opcode, "ADC", base, "X", self._a, crossed)


    def _adc_absolute_y(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._y)
        self._add_with_carry(operand)
        self._finish_indexed_update(address, opcode, "ADC", base, "Y", self._a, crossed)


    def _add_with_carry(self, operand):
        # The NES adds in binary even when the stored decimal flag is set.
        total = self._a + operand + self._carry

        # Signed overflow occurs when equal-sign inputs produce the opposite sign.
        self._overflow = bool(~(self._a ^ operand) & (self._a ^ total) & 0x80)
        self._carry = total > 0xFF
        self._a = total & 0xFF


    def _sbc_immediate(self, address, opcode):
        operand = self._fetch_byte()
        self._subtract_with_borrow(operand)
        self._finish_immediate_update(address, opcode, "SBC", operand, self._a)


    def _sbc_zero_page(self, address, opcode):
        destination = self._fetch_byte()
        operand = self._machine.read_byte(destination)
        self._subtract_with_borrow(operand)
        self._finish_zero_page_update(address, opcode, "SBC", destination, self._a)


    def _sbc_absolute(self, address, opcode):
        destination = self._fetch_word()
        operand = self._machine.read_byte(destination)
        self._subtract_with_borrow(operand)
        self._finish_absolute_update(address, opcode, "SBC", destination, self._a)


    def _sbc_absolute_x(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._x)
        self._subtract_with_borrow(operand)
        self._finish_indexed_update(address, opcode, "SBC", base, "X", self._a, crossed)


    def _sbc_absolute_y(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._y)
        self._subtract_with_borrow(operand)
        self._finish_indexed_update(address, opcode, "SBC", base, "Y", self._a, crossed)


    def _subtract_with_borrow(self, operand):
        # The NES subtracts in binary; a clear C represents an incoming borrow.
        difference = self._a - operand - (not self._carry)

        # C means no unsigned borrow; V detects signed subtraction overflow.
        self._overflow = bool((self._a ^ operand) & (self._a ^ difference) & 0x80)
        self._carry = difference >= 0
        self._a = difference & 0xFF


    def _bit_zero_page(self, address, opcode):
        # BIT reads the selected byte without changing the accumulator.
        source = self._fetch_byte()
        value = self._machine.read_byte(source)
        self._test_bits(value)

        # Reuse the fetched address for the instruction trace.
        self._cycles += 3
        self.log_instruction(address, (opcode, source), "BIT", f"${source:02X}")


    def _bit_absolute(self, address, opcode):
        # Read the byte addressed by the little-endian operand.
        source = self._fetch_word()
        value = self._machine.read_byte(source)
        self._test_bits(value)

        # Reuse the fetched address for the instruction trace.
        self._cycles += 4
        self.log_instruction(address, (opcode, source & 0xFF, source >> 8), "BIT", f"${source:04X}")


    def _test_bits(self, value):
        # N and V come from memory, while Z depends on the intersection with A.
        self._negative = bool(value & 0x80)
        self._overflow = bool(value & 0x40)
        self._zero = (self._a & value) == 0


    def _and_immediate(self, address, opcode):
        operand = self._fetch_byte()
        self._a &= operand
        self._finish_immediate_update(address, opcode, "AND", operand, self._a)


    def _and_zero_page(self, address, opcode):
        source = self._fetch_byte()
        self._a &= self._machine.read_byte(source)
        self._finish_zero_page_update(address, opcode, "AND", source, self._a)


    def _and_absolute(self, address, opcode):
        source = self._fetch_word()
        self._a &= self._machine.read_byte(source)
        self._finish_absolute_update(address, opcode, "AND", source, self._a)


    def _and_absolute_x(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._x)
        self._a &= operand
        self._finish_indexed_update(address, opcode, "AND", base, "X", self._a, crossed)


    def _and_absolute_y(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._y)
        self._a &= operand
        self._finish_indexed_update(address, opcode, "AND", base, "Y", self._a, crossed)


    def _ora_immediate(self, address, opcode):
        operand = self._fetch_byte()
        self._a |= operand
        self._finish_immediate_update(address, opcode, "ORA", operand, self._a)


    def _ora_zero_page(self, address, opcode):
        source = self._fetch_byte()
        self._a |= self._machine.read_byte(source)
        self._finish_zero_page_update(address, opcode, "ORA", source, self._a)


    def _ora_absolute(self, address, opcode):
        source = self._fetch_word()
        self._a |= self._machine.read_byte(source)
        self._finish_absolute_update(address, opcode, "ORA", source, self._a)


    def _ora_absolute_x(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._x)
        self._a |= operand
        self._finish_indexed_update(address, opcode, "ORA", base, "X", self._a, crossed)


    def _ora_absolute_y(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._y)
        self._a |= operand
        self._finish_indexed_update(address, opcode, "ORA", base, "Y", self._a, crossed)


    def _eor_immediate(self, address, opcode):
        operand = self._fetch_byte()
        self._a ^= operand
        self._finish_immediate_update(address, opcode, "EOR", operand, self._a)


    def _eor_zero_page(self, address, opcode):
        source = self._fetch_byte()
        self._a ^= self._machine.read_byte(source)
        self._finish_zero_page_update(address, opcode, "EOR", source, self._a)


    def _eor_absolute(self, address, opcode):
        source = self._fetch_word()
        self._a ^= self._machine.read_byte(source)
        self._finish_absolute_update(address, opcode, "EOR", source, self._a)


    def _eor_absolute_x(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._x)
        self._a ^= operand
        self._finish_indexed_update(address, opcode, "EOR", base, "X", self._a, crossed)


    def _eor_absolute_y(self, address, opcode):
        base, operand, crossed = self._read_absolute_indexed(self._y)
        self._a ^= operand
        self._finish_indexed_update(address, opcode, "EOR", base, "Y", self._a, crossed)


    def _finish_immediate_update(self, address, opcode, mnemonic, operand, value):
        # N and Z reflect the resulting register byte.
        self._negative = bool(value & 0x80)
        self._zero = value == 0

        # The trace uses the fetched operand without another memory read.
        self._cycles += 2
        self.log_instruction(address, (opcode, operand), mnemonic, f"#${operand:02X}")


    def _lda_immediate(self, address, opcode):
        self._a = self._fetch_byte()
        self._finish_immediate_update(address, opcode, "LDA", self._a, self._a)


    def _ldx_immediate(self, address, opcode):
        self._x = self._fetch_byte()
        self._finish_immediate_update(address, opcode, "LDX", self._x, self._x)


    def _ldy_immediate(self, address, opcode):
        self._y = self._fetch_byte()
        self._finish_immediate_update(address, opcode, "LDY", self._y, self._y)


    def _lda_absolute_x(self, address, opcode):
        base, self._a, crossed = self._read_absolute_indexed(self._x)
        self._finish_indexed_update(address, opcode, "LDA", base, "X", self._a, crossed)


    def _lda_absolute_y(self, address, opcode):
        base, self._a, crossed = self._read_absolute_indexed(self._y)
        self._finish_indexed_update(address, opcode, "LDA", base, "Y", self._a, crossed)


    def _ldx_absolute_y(self, address, opcode):
        base, self._x, crossed = self._read_absolute_indexed(self._y)
        self._finish_indexed_update(address, opcode, "LDX", base, "Y", self._x, crossed)


    def _ldy_absolute_x(self, address, opcode):
        base, self._y, crossed = self._read_absolute_indexed(self._x)
        self._finish_indexed_update(address, opcode, "LDY", base, "X", self._y, crossed)


    def _read_absolute_indexed(self, index):
        # Calculate the effective address and detect a page change, including 16-bit wrap.
        base = self._fetch_word()
        destination = (base + index) & 0xFFFF
        crossed = base >> 8 != destination >> 8

        # The functional model skips the provisional read on a page crossing.
        value = self._machine.read_byte(destination)
        return base, value, crossed


    def _finish_indexed_update(self, address, opcode, mnemonic, base, index_name, value, crossed):
        # N and Z reflect the resulting register byte.
        self._negative = bool(value & 0x80)
        self._zero = value == 0

        # Preserve the fetched base address for the trace and count page-crossing cost.
        self._cycles += 4 + crossed
        self.log_instruction(address, (opcode, base & 0xFF, base >> 8), mnemonic, f"${base:04X},{index_name}")


    def _lda_absolute(self, address, opcode):
        destination = self._fetch_word()
        self._a = self._machine.read_byte(destination)
        self._finish_absolute_update(address, opcode, "LDA", destination, self._a)


    def _ldx_absolute(self, address, opcode):
        destination = self._fetch_word()
        self._x = self._machine.read_byte(destination)
        self._finish_absolute_update(address, opcode, "LDX", destination, self._x)


    def _ldy_absolute(self, address, opcode):
        destination = self._fetch_word()
        self._y = self._machine.read_byte(destination)
        self._finish_absolute_update(address, opcode, "LDY", destination, self._y)


    def _finish_absolute_update(self, address, opcode, mnemonic, destination, value):
        # N and Z reflect the resulting register byte.
        self._negative = bool(value & 0x80)
        self._zero = value == 0

        # Use the fetched address for the trace without reading the device again.
        self._cycles += 4
        self.log_instruction(address, (opcode, destination & 0xFF, destination >> 8), mnemonic, f"${destination:04X}")


    def _sta_indexed_indirect(self, address, opcode):
        # X selects a pointer within zero page, including wrap at $FF.
        operand = self._fetch_byte()
        pointer = (operand + self._x) & 0xFF
        destination = self._read_zero_page_word(pointer)
        self._machine.write_byte(destination, self._a)

        # The functional model omits the discarded zero-page read.
        self._cycles += 6
        self.log_instruction(address, (opcode, operand), "STA", f"(${operand:02X},X)")


    def _sta_indirect_indexed(self, address, opcode):
        # Y indexes the address stored in a wrapping zero-page pointer.
        operand = self._fetch_byte()
        base = self._read_zero_page_word(operand)
        destination = (base + self._y) & 0xFFFF
        self._machine.write_byte(destination, self._a)

        # The functional model omits the provisional indexed read.
        self._cycles += 6
        self.log_instruction(address, (opcode, operand), "STA", f"(${operand:02X}),Y")


    def _read_zero_page_word(self, address):
        # Both pointer bytes are read through Machine within zero page.
        low = self._machine.read_byte(address)
        high = self._machine.read_byte((address + 1) & 0xFF)
        return low | (high << 8)


    def _sta_zero_page(self, address, opcode):
        self._store_zero_page(address, opcode, self._a, "STA")


    def _sta_zero_page_x(self, address, opcode):
        self._store_zero_page_indexed(address, opcode, self._a, self._x, "STA", "X")


    def _store_zero_page_indexed(self, address, opcode, value, index, mnemonic, index_name):
        # Indexing wraps inside zero page and omits the discarded hardware read.
        operand = self._fetch_byte()
        destination = (operand + index) & 0xFF
        self._machine.write_byte(destination, value)

        # Trace the original operand without rereading memory.
        self._cycles += 4
        self.log_instruction(address, (opcode, operand), mnemonic, f"${operand:02X},{index_name}")


    def _stx_zero_page(self, address, opcode):
        self._store_zero_page(address, opcode, self._x, "STX")


    def _stx_zero_page_y(self, address, opcode):
        self._store_zero_page_indexed(address, opcode, self._x, self._y, "STX", "Y")


    def _sty_zero_page(self, address, opcode):
        self._store_zero_page(address, opcode, self._y, "STY")


    def _sty_zero_page_x(self, address, opcode):
        self._store_zero_page_indexed(address, opcode, self._y, self._x, "STY", "X")


    def _store_zero_page(self, address, opcode, value, mnemonic):
        # An eight-bit operand addresses the first 256 bytes of CPU memory.
        destination = self._fetch_byte()
        self._machine.write_byte(destination, value)

        # Trace the fetched address without an additional memory read.
        self._cycles += 3
        self.log_instruction(address, (opcode, destination), mnemonic, f"${destination:02X}")


    def _sta_absolute_x(self, address, opcode):
        self._store_absolute_indexed(address, opcode, self._x, "X")


    def _sta_absolute_y(self, address, opcode):
        self._store_absolute_indexed(address, opcode, self._y, "Y")


    def _store_absolute_indexed(self, address, opcode, index, index_name):
        # Indexed addresses wrap in the CPU's 16-bit address space.
        base = self._fetch_word()
        destination = (base + index) & 0xFFFF
        self._machine.write_byte(destination, self._a)

        # Stores take five cycles, including the omitted provisional read.
        self._cycles += 5
        self.log_instruction(address, (opcode, base & 0xFF, base >> 8), "STA", f"${base:04X},{index_name}")


    def _sta_absolute(self, address, opcode):
        self._store_absolute(address, opcode, self._a, "STA")


    def _stx_absolute(self, address, opcode):
        self._store_absolute(address, opcode, self._x, "STX")


    def _sty_absolute(self, address, opcode):
        self._store_absolute(address, opcode, self._y, "STY")


    def _store_absolute(self, address, opcode, value, mnemonic):
        # The operand is a little-endian CPU address routed through Machine.
        destination = self._fetch_word()
        self._machine.write_byte(destination, value)

        # A rejected write stops execution before the instruction completes.
        self._cycles += 4
        self.log_instruction(address, (opcode, destination & 0xFF, destination >> 8), mnemonic, f"${destination:04X}")


    def _tsx(self, address, opcode):
        # TSX updates N and Z from the copied stack pointer.
        self._x = self._sp
        self._negative = bool(self._x & 0x80)
        self._zero = self._x == 0

        # The implied instruction takes two nominal cycles.
        self._cycles += 2
        self.log_instruction(address, (opcode,), "TSX")


    def _txs(self, address, opcode):
        self._sp = self._x
        self._cycles += 2
        self.log_instruction(address, (opcode,), "TXS")


    def _inc_zero_page(self, address, opcode):
        self._modify_zero_page(address, opcode, "INC", self._increment_byte)


    def _inc_zero_page_x(self, address, opcode):
        self._modify_zero_page(address, opcode, "INC", self._increment_byte, indexed=True)


    def _increment_byte(self, value):
        return (value + 1) & 0xFF


    def _dec_zero_page(self, address, opcode):
        self._modify_zero_page(address, opcode, "DEC", self._decrement_byte)


    def _dec_zero_page_x(self, address, opcode):
        self._modify_zero_page(address, opcode, "DEC", self._decrement_byte, indexed=True)


    def _decrement_byte(self, value):
        return (value - 1) & 0xFF


    def _asl_accumulator(self, address, opcode):
        self._a = self._shift_left(self._a)
        self._finish_register_update(address, opcode, "ASL", self._a)


    def _asl_zero_page(self, address, opcode):
        self._modify_zero_page(address, opcode, "ASL", self._shift_left)


    def _asl_absolute(self, address, opcode):
        self._modify_absolute(address, opcode, "ASL", self._shift_left)


    def _asl_absolute_x(self, address, opcode):
        self._modify_absolute(address, opcode, "ASL", self._shift_left, indexed=True)


    def _modify_absolute(self, address, opcode, mnemonic, operation, indexed=False):
        # Absolute,X wraps at 16 bits and omits the provisional indexed read.
        base = self._fetch_word()
        destination = (base + self._x) & 0xFFFF if indexed else base

        # The 6502 writes the original byte before writing the modified byte.
        original = self._machine.read_byte(destination)
        self._machine.write_byte(destination, original)
        value = operation(original)
        self._machine.write_byte(destination, value)

        # The resulting byte sets N/Z; the fetched address supplies the trace.
        self._negative = bool(value & 0x80)
        self._zero = value == 0
        self._cycles += 6 + indexed
        operand = f"${base:04X},X" if indexed else f"${base:04X}"
        self.log_instruction(address, (opcode, base & 0xFF, base >> 8), mnemonic, operand)


    def _shift_left(self, value):
        self._carry = bool(value & 0x80)
        return (value << 1) & 0xFF


    def _modify_zero_page(self, address, opcode, mnemonic, operation, indexed=False):
        # Indexed zero-page addresses wrap at $FF; the discarded read is omitted.
        operand = self._fetch_byte()
        destination = (operand + self._x) & 0xFF if indexed else operand

        # The 6502 writes the original byte as a bus cycle before writing the modified byte.
        # This first write does not change zero-page RAM.
        original = self._machine.read_byte(destination)
        self._machine.write_byte(destination, original)
        value = operation(original)
        self._machine.write_byte(destination, value)

        # The resulting byte sets N/Z; the fetched address supplies the trace.
        self._negative = bool(value & 0x80)
        self._zero = value == 0
        self._cycles += 5 + indexed
        operand_text = f"${operand:02X},X" if indexed else f"${operand:02X}"
        self.log_instruction(address, (opcode, operand), mnemonic, operand_text)


    def _lsr_accumulator(self, address, opcode):
        self._a = self._shift_right(self._a)
        self._finish_register_update(address, opcode, "LSR", self._a)


    def _lsr_zero_page(self, address, opcode):
        self._modify_zero_page(address, opcode, "LSR", self._shift_right)


    def _lsr_absolute(self, address, opcode):
        self._modify_absolute(address, opcode, "LSR", self._shift_right)


    def _lsr_absolute_x(self, address, opcode):
        self._modify_absolute(address, opcode, "LSR", self._shift_right, indexed=True)


    def _shift_right(self, value):
        self._carry = bool(value & 0x01)
        return value >> 1


    def _rol_accumulator(self, address, opcode):
        self._a = self._rotate_left(self._a)
        self._finish_register_update(address, opcode, "ROL", self._a)


    def _rol_zero_page(self, address, opcode):
        self._modify_zero_page(address, opcode, "ROL", self._rotate_left)


    def _rol_absolute(self, address, opcode):
        self._modify_absolute(address, opcode, "ROL", self._rotate_left)


    def _rol_absolute_x(self, address, opcode):
        self._modify_absolute(address, opcode, "ROL", self._rotate_left, indexed=True)


    def _rotate_left(self, value):
        # Preserve the incoming carry before replacing it with the outgoing bit.
        incoming_carry = self._carry
        self._carry = bool(value & 0x80)
        return ((value << 1) & 0xFF) | incoming_carry


    def _ror_accumulator(self, address, opcode):
        self._a = self._rotate_right(self._a)
        self._finish_register_update(address, opcode, "ROR", self._a)


    def _ror_zero_page(self, address, opcode):
        self._modify_zero_page(address, opcode, "ROR", self._rotate_right)


    def _ror_absolute(self, address, opcode):
        self._modify_absolute(address, opcode, "ROR", self._rotate_right)


    def _ror_absolute_x(self, address, opcode):
        self._modify_absolute(address, opcode, "ROR", self._rotate_right, indexed=True)


    def _rotate_right(self, value):
        # Preserve the incoming carry before replacing it with the outgoing bit.
        incoming_carry = self._carry
        self._carry = bool(value & 0x01)
        return (value >> 1) | (incoming_carry << 7)


    def _txa(self, address, opcode):
        self._a = self._x
        self._finish_register_update(address, opcode, "TXA", self._a)


    def _tya(self, address, opcode):
        self._a = self._y
        self._finish_register_update(address, opcode, "TYA", self._a)


    def _tax(self, address, opcode):
        self._x = self._a
        self._finish_register_update(address, opcode, "TAX", self._x)


    def _tay(self, address, opcode):
        self._y = self._a
        self._finish_register_update(address, opcode, "TAY", self._y)


    def _inx(self, address, opcode):
        self._x = (self._x + 1) & 0xFF
        self._finish_register_update(address, opcode, "INX", self._x)


    def _dex(self, address, opcode):
        self._x = (self._x - 1) & 0xFF
        self._finish_register_update(address, opcode, "DEX", self._x)


    def _iny(self, address, opcode):
        self._y = (self._y + 1) & 0xFF
        self._finish_register_update(address, opcode, "INY", self._y)


    def _dey(self, address, opcode):
        self._y = (self._y - 1) & 0xFF
        self._finish_register_update(address, opcode, "DEY", self._y)


    def _finish_register_update(self, address, opcode, mnemonic, value):
        # N and Z reflect the resulting byte.
        self._negative = bool(value & 0x80)
        self._zero = value == 0

        # The implied instruction takes two nominal cycles.
        self._cycles += 2
        self.log_instruction(address, (opcode,), mnemonic)


    def _beq(self, address, opcode):
        self._branch(address, opcode, "BEQ", self._zero)


    def _bne(self, address, opcode):
        self._branch(address, opcode, "BNE", not self._zero)


    def _bpl(self, address, opcode):
        self._branch(address, opcode, "BPL", not self._negative)


    def _bmi(self, address, opcode):
        self._branch(address, opcode, "BMI", self._negative)


    def _bcc(self, address, opcode):
        self._branch(address, opcode, "BCC", not self._carry)


    def _bcs(self, address, opcode):
        self._branch(address, opcode, "BCS", self._carry)


    def _bvc(self, address, opcode):
        self._branch(address, opcode, "BVC", not self._overflow)


    def _bvs(self, address, opcode):
        self._branch(address, opcode, "BVS", self._overflow)


    def _branch(self, address, opcode, mnemonic, condition):
        # The signed displacement is relative to PC after fetching the operand.
        operand = self._fetch_byte()
        displacement = operand if operand < 0x80 else operand - 0x100
        target = (self._pc + displacement) & 0xFFFF

        # A taken branch costs one extra cycle, plus one for crossing a page.
        self._cycles += 2
        if condition:
            self._cycles += 1
            if self._pc >> 8 != target >> 8:
                self._cycles += 1
            self._pc = target

        # The trace uses the already fetched operand and calculated target.
        self.log_instruction(address, (opcode, operand), mnemonic, f"${target:04X}")


    def _clc(self, address, opcode):
        """Clear the carry flag used by arithmetic and rotates."""
        self._carry = False
        self._cycles += 2
        self.log_instruction(address, (opcode,), "CLC")


    def _sec(self, address, opcode):
        """Set the carry flag used by arithmetic and rotates."""
        self._carry = True
        self._cycles += 2
        self.log_instruction(address, (opcode,), "SEC")


    def _cli(self, address, opcode):
        """Clear the interrupt-disable flag used to mask IRQs."""
        self._interrupt_disable = False
        self._cycles += 2
        self.log_instruction(address, (opcode,), "CLI")


    def _sei(self, address, opcode):
        """Set the interrupt-disable flag used to mask IRQs."""
        self._interrupt_disable = True
        self._cycles += 2
        self.log_instruction(address, (opcode,), "SEI")


    def _clv(self, address, opcode):
        """Clear the overflow flag used to report signed arithmetic overflow."""
        self._overflow = False
        self._cycles += 2
        self.log_instruction(address, (opcode,), "CLV")


    def _cld(self, address, opcode):
        """Clear the decimal flag stored in the status register."""
        self._decimal = False
        self._cycles += 2
        self.log_instruction(address, (opcode,), "CLD")


    def _nop(self, address, opcode):
        """Complete the no-op after the shared fetch advances PC."""
        self._cycles += 2
        self.log_instruction(address, (opcode,), "NOP")


    def _sed(self, address, opcode):
        """Set the decimal flag, which the NES CPU stores even with binary arithmetic."""
        self._decimal = True
        self._cycles += 2
        self.log_instruction(address, (opcode,), "SED")


    # The opcode is the tuple index. None marks an unimplemented instruction.
    _instruction_handlers = (
        # $00-$0F
        None,  # $00
        None,  # $01
        None,  # $02
        None,  # $03
        None,  # $04
        _ora_zero_page,  # $05
        _asl_zero_page,  # $06
        None,  # $07
        None,  # $08
        _ora_immediate,  # $09
        _asl_accumulator,  # $0A
        None,  # $0B
        None,  # $0C
        _ora_absolute,  # $0D
        _asl_absolute,  # $0E
        None,  # $0F

        # $10-$1F
        _bpl,  # $10
        None,  # $11
        None,  # $12
        None,  # $13
        None,  # $14
        None,  # $15
        None,  # $16
        None,  # $17
        _clc,  # $18
        _ora_absolute_y,  # $19
        None,  # $1A
        None,  # $1B
        None,  # $1C
        _ora_absolute_x,  # $1D
        _asl_absolute_x,  # $1E
        None,  # $1F

        # $20-$2F
        _jsr_absolute,  # $20
        None,  # $21
        None,  # $22
        None,  # $23
        _bit_zero_page,  # $24
        _and_zero_page,  # $25
        _rol_zero_page,  # $26
        None,  # $27
        None,  # $28
        _and_immediate,  # $29
        _rol_accumulator,  # $2A
        None,  # $2B
        _bit_absolute,  # $2C
        _and_absolute,  # $2D
        _rol_absolute,  # $2E
        None,  # $2F

        # $30-$3F
        _bmi,  # $30
        None,  # $31
        None,  # $32
        None,  # $33
        None,  # $34
        None,  # $35
        None,  # $36
        None,  # $37
        _sec,  # $38
        _and_absolute_y,  # $39
        None,  # $3A
        None,  # $3B
        None,  # $3C
        _and_absolute_x,  # $3D
        _rol_absolute_x,  # $3E
        None,  # $3F

        # $40-$4F
        None,  # $40
        None,  # $41
        None,  # $42
        None,  # $43
        None,  # $44
        _eor_zero_page,  # $45
        _lsr_zero_page,  # $46
        None,  # $47
        None,  # $48
        _eor_immediate,  # $49
        _lsr_accumulator,  # $4A
        None,  # $4B
        _jmp_absolute,  # $4C
        _eor_absolute,  # $4D
        _lsr_absolute,  # $4E
        None,  # $4F

        # $50-$5F
        _bvc,  # $50
        None,  # $51
        None,  # $52
        None,  # $53
        None,  # $54
        None,  # $55
        None,  # $56
        None,  # $57
        _cli,  # $58
        _eor_absolute_y,  # $59
        None,  # $5A
        None,  # $5B
        None,  # $5C
        _eor_absolute_x,  # $5D
        _lsr_absolute_x,  # $5E
        None,  # $5F

        # $60-$6F
        _rts,  # $60
        None,  # $61
        None,  # $62
        None,  # $63
        None,  # $64
        _adc_zero_page,  # $65
        _ror_zero_page,  # $66
        None,  # $67
        None,  # $68
        _adc_immediate,  # $69
        _ror_accumulator,  # $6A
        None,  # $6B
        _jmp_indirect,  # $6C
        _adc_absolute,  # $6D
        _ror_absolute,  # $6E
        None,  # $6F

        # $70-$7F
        _bvs,  # $70
        None,  # $71
        None,  # $72
        None,  # $73
        None,  # $74
        None,  # $75
        None,  # $76
        None,  # $77
        _sei,  # $78
        _adc_absolute_y,  # $79
        None,  # $7A
        None,  # $7B
        None,  # $7C
        _adc_absolute_x,  # $7D
        _ror_absolute_x,  # $7E
        None,  # $7F

        # $80-$8F
        None,  # $80
        _sta_indexed_indirect,  # $81
        None,  # $82
        None,  # $83
        _sty_zero_page,  # $84
        _sta_zero_page,  # $85
        _stx_zero_page,  # $86
        None,  # $87
        _dey,  # $88
        None,  # $89
        _txa,  # $8A
        None,  # $8B
        _sty_absolute,  # $8C
        _sta_absolute,  # $8D
        _stx_absolute,  # $8E
        None,  # $8F

        # $90-$9F
        _bcc,  # $90
        _sta_indirect_indexed,  # $91
        None,  # $92
        None,  # $93
        _sty_zero_page_x,  # $94
        _sta_zero_page_x,  # $95
        _stx_zero_page_y,  # $96
        None,  # $97
        _tya,  # $98
        _sta_absolute_y,  # $99
        _txs,  # $9A
        None,  # $9B
        None,  # $9C
        _sta_absolute_x,  # $9D
        None,  # $9E
        None,  # $9F

        # $A0-$AF
        _ldy_immediate,  # $A0
        _lda_indexed_indirect,  # $A1
        _ldx_immediate,  # $A2
        None,  # $A3
        _ldy_zero_page,  # $A4
        _lda_zero_page,  # $A5
        _ldx_zero_page,  # $A6
        None,  # $A7
        _tay,  # $A8
        _lda_immediate,  # $A9
        _tax,  # $AA
        None,  # $AB
        _ldy_absolute,  # $AC
        _lda_absolute,  # $AD
        _ldx_absolute,  # $AE
        None,  # $AF

        # $B0-$BF
        _bcs,  # $B0
        _lda_indirect_indexed,  # $B1
        None,  # $B2
        None,  # $B3
        _ldy_zero_page_x,  # $B4
        _lda_zero_page_x,  # $B5
        _ldx_zero_page_y,  # $B6
        None,  # $B7
        _clv,  # $B8
        _lda_absolute_y,  # $B9
        _tsx,  # $BA
        None,  # $BB
        _ldy_absolute_x,  # $BC
        _lda_absolute_x,  # $BD
        _ldx_absolute_y,  # $BE
        None,  # $BF

        # $C0-$CF
        _cpy_immediate,  # $C0
        None,  # $C1
        None,  # $C2
        None,  # $C3
        None,  # $C4
        None,  # $C5
        _dec_zero_page,  # $C6
        None,  # $C7
        _iny,  # $C8
        _cmp_immediate,  # $C9
        _dex,  # $CA
        None,  # $CB
        _cpy_absolute,  # $CC
        _cmp_absolute,  # $CD
        None,  # $CE
        None,  # $CF

        # $D0-$DF
        _bne,  # $D0
        None,  # $D1
        None,  # $D2
        None,  # $D3
        None,  # $D4
        None,  # $D5
        _dec_zero_page_x,  # $D6
        None,  # $D7
        _cld,  # $D8
        _cmp_absolute_y,  # $D9
        None,  # $DA
        None,  # $DB
        None,  # $DC
        _cmp_absolute_x,  # $DD
        None,  # $DE
        None,  # $DF

        # $E0-$EF
        _cpx_immediate,  # $E0
        None,  # $E1
        None,  # $E2
        None,  # $E3
        None,  # $E4
        _sbc_zero_page,  # $E5
        _inc_zero_page,  # $E6
        None,  # $E7
        _inx,  # $E8
        _sbc_immediate,  # $E9
        _nop,  # $EA
        None,  # $EB
        _cpx_absolute,  # $EC
        _sbc_absolute,  # $ED
        None,  # $EE
        None,  # $EF

        # $F0-$FF
        _beq,  # $F0
        None,  # $F1
        None,  # $F2
        None,  # $F3
        None,  # $F4
        None,  # $F5
        _inc_zero_page_x,  # $F6
        None,  # $F7
        _sed,  # $F8
        _sbc_absolute_y,  # $F9
        None,  # $FA
        None,  # $FB
        None,  # $FC
        _sbc_absolute_x,  # $FD
        None,  # $FE
        None,  # $FF
    )
