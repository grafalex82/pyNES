"""Provide minimal PPU registers, pattern data, nametable memory, and palette RAM."""


class PPU:
    """Minimal PPU boundary; retained writes have no hardware register effects."""

    def __init__(self, chr_rom, chr_size, nametable_ram, mirroring):
        self._last_writes = [None] * 8
        self._next_status = 0x00
        self._chr_rom = chr_rom
        self._chr_size = chr_size
        self._nametable_ram = nametable_ram
        self._mirroring = mirroring
        self._palette_ram = bytearray(32)


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


    def _nametable_offset(self, address):
        # Cartridge wiring selects which logical nametable address bit reaches CIRAM A10.
        if self._mirroring == "horizontal":
            page = (address >> 11) & 1
        elif self._mirroring == "vertical":
            page = (address >> 10) & 1
        else:
            raise NotImplementedError(f"PPU nametable mirroring {self._mirroring} is not implemented")
        return (page << 10) | (address & 0x03FF)


    def _palette_offset(self, address):
        # Palette RAM repeats every 32 bytes. Sprite palette entries 0x10/14/18/1C correspond to pixel
        # index 0 (transparent), so they need no separate displayed colors. The PPU maps these addresses
        # to 0x00/04/08/0C in the background palette; even direct memory reads and writes share those bytes.
        offset = address & 0x1F
        if offset in (0x10, 0x14, 0x18, 0x1C):
            offset -= 0x10
        return offset


    def read_memory(self, address):
        # NROM maps its two consecutive 4 KiB pattern tables directly to CHR ROM.
        if address < 0x2000:
            return self._pattern_rom().read_byte(address)

        # $3000-$3EFF mirrors $2000-$2EFF, using the same lower address bits.
        if address < 0x3F00:
            return self._nametable_ram.read_byte(self._nametable_offset(address))

        # PPU palette memory holds six-bit color codes, including mirrored addresses.
        if address < 0x4000:
            return self._palette_ram[self._palette_offset(address)]

        # Only the 14-bit PPU address space is implemented.
        raise NotImplementedError(f"PPU memory read at address 0x{address:04X} is not implemented")


    def write_memory(self, address, value):
        # Writes reach the ROM device's diagnostic trap instead of changing pattern data.
        if address < 0x2000:
            self._pattern_rom().write_byte(address, value)
            return

        # Nametable aliases select the same byte of the two physical RAM pages.
        if address < 0x3F00:
            self._nametable_ram.write_byte(self._nametable_offset(address), value)
            return

        # Store only the six color bits at the shared palette address.
        if address < 0x4000:
            self._palette_ram[self._palette_offset(address)] = value & 0x3F
            return

        # Only the 14-bit PPU address space is implemented.
        raise NotImplementedError(f"PPU memory write at address 0x{address:04X} is not implemented")
