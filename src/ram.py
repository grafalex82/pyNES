"""Store writable memory independently of CPU address routing."""


class RAM:
    """Writable memory with byte access and zero-filled initial contents.
    Byte offsets start at zero; CPU address routing and mirroring belong to Machine.
    """

    def __init__(self, size):
        # Zero filling makes runs reproducible; hardware power-up contents are not guaranteed.
        self._ram = bytearray(size)


    def read_byte(self, offset):
        return self._ram[offset]


    def write_byte(self, offset, value):
        # Reject values that do not fit on the eight-bit data bus.
        if not 0 <= value <= 0xFF:
            raise ValueError(f"RAM byte value {value} is outside 0..255")

        # Store only after validation so a rejected write leaves RAM unchanged.
        self._ram[offset] = value
