"""Provide minimal PPU registers and access to cartridge pattern data."""


class PPU:
    """Minimal PPU boundary; retained writes have no hardware register effects."""

    def __init__(self, chr_rom, chr_size):
        self._last_writes = [None] * 8
        self._next_status = 0x00
        self._chr_rom = chr_rom
        self._chr_size = chr_size


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


    def _pattern_rom(self):
        # Defer unsupported video configurations so PRG-only programs can still execute.
        if self._chr_size == 0:
            raise NotImplementedError("Mapper 0 CHR RAM is not implemented")
        if self._chr_size != 8192:
            raise NotImplementedError(f"Mapper 0 CHR ROM size {self._chr_size} bytes is not implemented")
        return self._chr_rom


    def read_memory(self, address):
        # NROM maps its two consecutive 4 KiB pattern tables directly to CHR ROM.
        if address < 0x2000:
            return self._pattern_rom().read_byte(address)

        # Nametable and palette memory are separate, unimplemented parts of the PPU address space.
        raise NotImplementedError(f"PPU memory read at address 0x{address:04X} is not implemented")


    def write_memory(self, address, value):
        # Writes reach the ROM device's diagnostic trap instead of changing pattern data.
        if address < 0x2000:
            self._pattern_rom().write_byte(address, value)
            return

        # Other PPU memory areas remain unimplemented until their own routing is introduced.
        raise NotImplementedError(f"PPU memory write at address 0x{address:04X} is not implemented")
