"""Retain CPU writes to the eight PPU register offsets for inspection."""


class PPU:
    """Minimal PPU boundary; retained writes have no hardware register effects."""

    def __init__(self):
        self._last_writes = [None] * 8


    @property
    def last_writes(self):
        """Return the last byte per offset, or None where no write has occurred."""
        return tuple(self._last_writes)


    def read_byte(self, offset):
        raise NotImplementedError(f"PPU read at register offset 0x{offset:02X} is not implemented")


    def write_byte(self, offset, value):
        self._last_writes[offset] = value
