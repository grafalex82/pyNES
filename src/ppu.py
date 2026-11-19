"""Provide minimal CPU-facing PPU register behavior."""


class PPU:
    """Minimal PPU boundary; retained writes have no hardware register effects."""

    def __init__(self):
        self._last_writes = [None] * 8
        self._next_status = 0x00


    @property
    def last_writes(self):
        """Return the last byte per offset, or None where no write has occurred."""
        return tuple(self._last_writes)


    def read_byte(self, offset):
        # Alternate the vblank bit on status reads so polling can progress without video timing.
        if offset == 2:
            status = self._next_status
            self._next_status ^= 0x80
            return status

        # Other PPU register reads remain explicit missing behavior.
        raise NotImplementedError(f"PPU read at register offset 0x{offset:02X} is not implemented")


    def write_byte(self, offset, value):
        self._last_writes[offset] = value
