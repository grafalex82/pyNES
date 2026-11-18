"""Expose NES CPU registers, separately stored status flags, and functional startup."""


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
