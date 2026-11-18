"""Expose NES CPU registers and separately stored status flags."""


class CPU:
    """CPU state with byte registers A/X/Y/SP and a 16-bit program counter.

    Callers supply valid register and flag values through properties. Construction
    currently initializes storage only; functional startup and reset are separate tasks.
    B is software inspection state rather than a physical processor latch.
    """

    def __init__(self, machine):
        # Future CPU memory accesses use Machine's address routing.
        self._machine = machine

        # These storage defaults precede the functional startup/reset implementation.
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


    @property
    def a(self):
        return self._a


    @a.setter
    def a(self, value):
        self._a = value


    @property
    def x(self):
        return self._x


    @x.setter
    def x(self, value):
        self._x = value


    @property
    def y(self):
        return self._y


    @y.setter
    def y(self, value):
        self._y = value


    @property
    def sp(self):
        return self._sp


    @sp.setter
    def sp(self, value):
        self._sp = value


    @property
    def pc(self):
        return self._pc


    @pc.setter
    def pc(self, value):
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
        # Replace all seven status fields; input bit 5 has no stored counterpart.
        self._carry = bool(value & 0x01)
        self._zero = bool(value & 0x02)
        self._interrupt_disable = bool(value & 0x04)
        self._decimal = bool(value & 0x08)
        self._break_flag = bool(value & 0x10)
        self._overflow = bool(value & 0x40)
        self._negative = bool(value & 0x80)
