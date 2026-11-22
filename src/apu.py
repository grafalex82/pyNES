"""Provide a minimal CPU-facing audio register boundary."""

import logging


logger = logging.getLogger("apu")
_REGISTERS = (0x10, 0x11, 0x12, 0x13, 0x15)


class APU:
    """Accept selected writes and report inactive status without emulating audio."""

    def read_byte(self, offset):
        # Other offsets must remain explicit missing behavior even when APU is accessed directly.
        if offset not in _REGISTERS:
            raise NotImplementedError(f"APU read at register offset 0x{offset:02X} is not implemented")

        # A fixed zero approximates open bus and reports all audio channels and IRQs inactive.
        return 0x00


    def write_byte(self, offset, value):
        # Other offsets must remain explicit missing behavior even when APU is accessed directly.
        if offset not in _REGISTERS and offset not in (0x00, 0x04, 0x06, 0x08, 0x0C, 0x17):
            raise NotImplementedError(f"APU write at register offset 0x{offset:02X} is not implemented")

        # The dummy has no sample fetching, register effects, or sound output.
        logger.debug("Ignored APU write at register offset 0x%02X: 0x%02X", offset, value)
