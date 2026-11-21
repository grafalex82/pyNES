"""Provide minimal PPU registers, pattern data, nametable memory, and palette RAM."""

from nes_palette import NES_COLORS


class PPU:
    """Minimal PPU boundary with an address latch and retained register writes."""

    def __init__(self, chr_rom, chr_size, nametable_ram, mirroring):
        self._last_writes = [None] * 8
        self._next_status = 0x00
        self._chr_rom = chr_rom
        self._chr_size = chr_size
        self._nametable_ram = nametable_ram
        self._mirroring = mirroring
        self._palette_ram = bytearray(32)
        self._vram_read_buffer = 0
        self._vram_address = 0
        self._temporary_address = 0
        self._awaiting_second_write = False
        self._write_ppuctrl(0)


    @property
    def last_writes(self):
        """Return the last byte per offset, or None where no write has occurred."""
        return tuple(self._last_writes)


    def read_byte(self, offset):
        # PPUSTATUS ($2002) reports status and resets the address write pair.
        if offset == 2:
            return self._read_ppustatus()

        # PPUDATA ($2007) reads video memory and advances the selected address.
        if offset == 7:
            return self._read_ppudata()

        # Other PPU register reads remain explicit missing behavior.
        raise NotImplementedError(f"PPU read at register offset 0x{offset:02X} is not implemented")


    def write_byte(self, offset, value):
        # Retain all writes for inspection, including writes to the read-only hardware status register.
        self._last_writes[offset] = value

        # PPUCTRL ($2000) selects video addressing and rendering settings.
        if offset == 0:
            self._write_ppuctrl(value)

        # PPUADDR ($2006) selects the PPU video address in two writes.
        if offset == 6:
            self._write_ppuaddr(value)

        # PPUDATA ($2007) writes video memory and advances the selected address.
        if offset == 7:
            self._write_ppudata(value)


    def _write_ppuctrl(self, value):
        # Decode VPHB SINN into independent settings; NN selects the base nametable coordinates.
        self._base_nametable_x = bool(value & 0x01)
        self._base_nametable_y = bool(value & 0x02)
        self._increment_32 = bool(value & 0x04)
        self._sprite_pattern_table_high = bool(value & 0x08)
        self._background_pattern_table_high = bool(value & 0x10)
        self._sprite_height_16 = bool(value & 0x20)
        self._ext_output_enabled = bool(value & 0x40)
        self._nmi_enabled = bool(value & 0x80)


    def _read_ppustatus(self):
        # Reset the address write pair and alternate vblank until video timing is implemented.
        self._awaiting_second_write = False
        status = self._next_status
        self._next_status ^= 0x80
        return status


    def _write_ppuaddr(self, value):
        # The first write selects the upper six address bits; the second commits the full address.
        if not self._awaiting_second_write:
            self._temporary_address = (self._temporary_address & 0x00FF) | ((value & 0x3F) << 8)
        else:
            self._temporary_address = (self._temporary_address & 0x7F00) | value
            self._vram_address = self._temporary_address
        self._awaiting_second_write = not self._awaiting_second_write


    def _read_ppudata(self):
        # CHR and nametable reads return the previous buffered byte while loading the addressed byte for the next read.
        # Palette reads return the color immediately, but refill the buffer from the nametable address $1000 below.
        # Changing PPUADDR does not clear this buffer, so a program normally discards its first non-palette read.
        address = self._vram_address & 0x3FFF
        if address < 0x3F00:
            result = self._vram_read_buffer
            self._vram_read_buffer = self.read_vram(address)
        else:
            result = self.read_vram(address)
            self._vram_read_buffer = self.read_vram(address - 0x1000)

        # Failed reads propagate without advancing the video address.
        self._advance_vram_address()
        return result


    def _write_ppudata(self, value):
        # PPU memory sees the low 14 bits of the internal 15-bit video address.
        self.write_vram(self._vram_address & 0x3FFF, value)

        # Rejected writes propagate without advancing the video address.
        self._advance_vram_address()


    def _advance_vram_address(self):
        # PPUCTRL selects the step for both reads and writes; the internal address is 15 bits wide.
        increment = 32 if self._increment_32 else 1
        self._vram_address = (self._vram_address + increment) & 0x7FFF


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


    def render_frame(self):
        """Render the backdrop as a native-size frame of packed RGB bytes."""
        # Until layers are implemented, every pixel uses the universal backdrop color.
        color = NES_COLORS[self.read_vram(0x3F00)].to_bytes(3, "big")
        return color * (256 * 240)


    def read_vram(self, address):
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


    def write_vram(self, address, value):
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
