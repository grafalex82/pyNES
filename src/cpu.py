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


    def _lda_immediate(self, address, opcode):
        self._a = self._fetch_byte()
        self._finish_immediate_load(address, opcode, "LDA", self._a)


    def _ldx_immediate(self, address, opcode):
        self._x = self._fetch_byte()
        self._finish_immediate_load(address, opcode, "LDX", self._x)


    def _ldy_immediate(self, address, opcode):
        self._y = self._fetch_byte()
        self._finish_immediate_load(address, opcode, "LDY", self._y)


    def _finish_immediate_load(self, address, opcode, mnemonic, value):
        # Loads set N from bit 7 and Z from the entire byte, leaving the other flags untouched.
        self._negative = bool(value & 0x80)
        self._zero = value == 0

        # Immediate loads take two nominal cycles; the fetched value also supplies the trace.
        self._cycles += 2
        self.log_instruction(address, (opcode, value), mnemonic, f"#${value:02X}")


    def _lda_absolute(self, address, opcode):
        destination = self._fetch_word()
        self._a = self._machine.read_byte(destination)
        self._finish_absolute_load(address, opcode, "LDA", destination, self._a)


    def _ldx_absolute(self, address, opcode):
        destination = self._fetch_word()
        self._x = self._machine.read_byte(destination)
        self._finish_absolute_load(address, opcode, "LDX", destination, self._x)


    def _ldy_absolute(self, address, opcode):
        destination = self._fetch_word()
        self._y = self._machine.read_byte(destination)
        self._finish_absolute_load(address, opcode, "LDY", destination, self._y)


    def _finish_absolute_load(self, address, opcode, mnemonic, destination, value):
        # Loads update N and Z from the value returned by the addressed device.
        self._negative = bool(value & 0x80)
        self._zero = value == 0

        # Use the fetched address for the trace without reading the device again.
        self._cycles += 4
        self.log_instruction(address, (opcode, destination & 0xFF, destination >> 8), mnemonic, f"${destination:04X}")


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


    def _txa(self, address, opcode):
        self._a = self._x
        self._finish_register_transfer(address, opcode, "TXA", self._a)


    def _tya(self, address, opcode):
        self._a = self._y
        self._finish_register_transfer(address, opcode, "TYA", self._a)


    def _tax(self, address, opcode):
        self._x = self._a
        self._finish_register_transfer(address, opcode, "TAX", self._x)


    def _tay(self, address, opcode):
        self._y = self._a
        self._finish_register_transfer(address, opcode, "TAY", self._y)


    def _finish_register_transfer(self, address, opcode, mnemonic, value):
        # Register transfers set N and Z from the transferred byte.
        self._negative = bool(value & 0x80)
        self._zero = value == 0

        # The implied instruction takes two nominal cycles.
        self._cycles += 2
        self.log_instruction(address, (opcode,), mnemonic)


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
        None,  # $05
        None,  # $06
        None,  # $07
        None,  # $08
        None,  # $09
        None,  # $0A
        None,  # $0B
        None,  # $0C
        None,  # $0D
        None,  # $0E
        None,  # $0F

        # $10-$1F
        None,  # $10
        None,  # $11
        None,  # $12
        None,  # $13
        None,  # $14
        None,  # $15
        None,  # $16
        None,  # $17
        _clc,  # $18
        None,  # $19
        None,  # $1A
        None,  # $1B
        None,  # $1C
        None,  # $1D
        None,  # $1E
        None,  # $1F

        # $20-$2F
        None,  # $20
        None,  # $21
        None,  # $22
        None,  # $23
        None,  # $24
        None,  # $25
        None,  # $26
        None,  # $27
        None,  # $28
        None,  # $29
        None,  # $2A
        None,  # $2B
        None,  # $2C
        None,  # $2D
        None,  # $2E
        None,  # $2F

        # $30-$3F
        None,  # $30
        None,  # $31
        None,  # $32
        None,  # $33
        None,  # $34
        None,  # $35
        None,  # $36
        None,  # $37
        _sec,  # $38
        None,  # $39
        None,  # $3A
        None,  # $3B
        None,  # $3C
        None,  # $3D
        None,  # $3E
        None,  # $3F

        # $40-$4F
        None,  # $40
        None,  # $41
        None,  # $42
        None,  # $43
        None,  # $44
        None,  # $45
        None,  # $46
        None,  # $47
        None,  # $48
        None,  # $49
        None,  # $4A
        None,  # $4B
        None,  # $4C
        None,  # $4D
        None,  # $4E
        None,  # $4F

        # $50-$5F
        None,  # $50
        None,  # $51
        None,  # $52
        None,  # $53
        None,  # $54
        None,  # $55
        None,  # $56
        None,  # $57
        _cli,  # $58
        None,  # $59
        None,  # $5A
        None,  # $5B
        None,  # $5C
        None,  # $5D
        None,  # $5E
        None,  # $5F

        # $60-$6F
        None,  # $60
        None,  # $61
        None,  # $62
        None,  # $63
        None,  # $64
        None,  # $65
        None,  # $66
        None,  # $67
        None,  # $68
        None,  # $69
        None,  # $6A
        None,  # $6B
        None,  # $6C
        None,  # $6D
        None,  # $6E
        None,  # $6F

        # $70-$7F
        None,  # $70
        None,  # $71
        None,  # $72
        None,  # $73
        None,  # $74
        None,  # $75
        None,  # $76
        None,  # $77
        _sei,  # $78
        None,  # $79
        None,  # $7A
        None,  # $7B
        None,  # $7C
        None,  # $7D
        None,  # $7E
        None,  # $7F

        # $80-$8F
        None,  # $80
        None,  # $81
        None,  # $82
        None,  # $83
        None,  # $84
        None,  # $85
        None,  # $86
        None,  # $87
        None,  # $88
        None,  # $89
        _txa,  # $8A
        None,  # $8B
        _sty_absolute,  # $8C
        _sta_absolute,  # $8D
        _stx_absolute,  # $8E
        None,  # $8F

        # $90-$9F
        None,  # $90
        None,  # $91
        None,  # $92
        None,  # $93
        None,  # $94
        None,  # $95
        None,  # $96
        None,  # $97
        _tya,  # $98
        None,  # $99
        _txs,  # $9A
        None,  # $9B
        None,  # $9C
        None,  # $9D
        None,  # $9E
        None,  # $9F

        # $A0-$AF
        _ldy_immediate,  # $A0
        None,  # $A1
        _ldx_immediate,  # $A2
        None,  # $A3
        None,  # $A4
        None,  # $A5
        None,  # $A6
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
        None,  # $B0
        None,  # $B1
        None,  # $B2
        None,  # $B3
        None,  # $B4
        None,  # $B5
        None,  # $B6
        None,  # $B7
        _clv,  # $B8
        None,  # $B9
        _tsx,  # $BA
        None,  # $BB
        None,  # $BC
        None,  # $BD
        None,  # $BE
        None,  # $BF

        # $C0-$CF
        None,  # $C0
        None,  # $C1
        None,  # $C2
        None,  # $C3
        None,  # $C4
        None,  # $C5
        None,  # $C6
        None,  # $C7
        None,  # $C8
        None,  # $C9
        None,  # $CA
        None,  # $CB
        None,  # $CC
        None,  # $CD
        None,  # $CE
        None,  # $CF

        # $D0-$DF
        None,  # $D0
        None,  # $D1
        None,  # $D2
        None,  # $D3
        None,  # $D4
        None,  # $D5
        None,  # $D6
        None,  # $D7
        _cld,  # $D8
        None,  # $D9
        None,  # $DA
        None,  # $DB
        None,  # $DC
        None,  # $DD
        None,  # $DE
        None,  # $DF

        # $E0-$EF
        None,  # $E0
        None,  # $E1
        None,  # $E2
        None,  # $E3
        None,  # $E4
        None,  # $E5
        None,  # $E6
        None,  # $E7
        None,  # $E8
        None,  # $E9
        _nop,  # $EA
        None,  # $EB
        None,  # $EC
        None,  # $ED
        None,  # $EE
        None,  # $EF

        # $F0-$FF
        None,  # $F0
        None,  # $F1
        None,  # $F2
        None,  # $F3
        None,  # $F4
        None,  # $F5
        None,  # $F6
        None,  # $F7
        _sed,  # $F8
        None,  # $F9
        None,  # $FA
        None,  # $FB
        None,  # $FC
        None,  # $FD
        None,  # $FE
        None,  # $FF
    )
