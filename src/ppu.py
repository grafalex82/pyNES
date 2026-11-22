"""Provide minimal PPU registers, video memory, and approximate frame timing."""

import logging

from nes_palette import NES_COLORS


logger = logging.getLogger("ppu")

FRAME_CPU_CYCLES = 29781
VBLANK_START_CPU_CYCLE = 27394
VBLANK_END_CPU_CYCLE = 29667


class PPU:
    """Minimal PPU boundary with an address latch and retained register writes."""

    def __init__(self, chr_rom, chr_size, nametable_ram, mirroring):
        self._last_writes = [None] * 8
        self._frame_cycle = 0
        self._vblank = False
        self._nmi_pending = False
        self._nmi_enabled = False
        self._background_enabled = False
        self._sprites_enabled = False
        self._frame_output_enabled = False
        self._completed_frame = None
        self._completed_background = None
        self._published_frames = 0
        self._chr_rom = chr_rom
        self._chr_size = chr_size
        self._nametable_ram = nametable_ram
        self._mirroring = mirroring
        self._palette_ram = bytearray(32)
        self._oam = bytearray(256)
        self._oam_address = 0
        self._vram_read_buffer = 0
        self._vram_address = 0
        self._temporary_address = 0
        self._awaiting_second_write = False
        self._write_ppuctrl(0)


    @property
    def last_writes(self):
        """Return the last byte per offset, or None where no write has occurred."""
        return tuple(self._last_writes)


    @property
    def completed_frame(self):
        """Return the latest (sequence number, RGB frame), or None before the first capture."""
        return self._completed_frame


    @property
    def completed_background(self):
        """Return (sequence, tiles, attributes, 16 packed RGB colors), or None before capture.

        The palette follows $3F00-$3F0F; background pattern index zero uses entry 0 for every subpalette.
        """
        return self._completed_background


    def enable_frame_output(self):
        """Capture completed frames at subsequent vblank entries."""
        self._frame_output_enabled = True


    def take_nmi(self):
        """Consume a latched NMI request, if one has occurred."""
        pending = self._nmi_pending
        self._nmi_pending = False
        return pending


    def read_byte(self, offset):
        # PPUSTATUS ($2002) reports status and resets the address write pair.
        if offset == 2:
            return self._read_ppustatus()

        # OAMDATA reads leave the selected object-memory address unchanged.
        if offset == 4:
            return self._oam[self._oam_address]

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

        # PPUMASK ($2001) controls whether the background and sprite layers are visible.
        if offset == 1:
            self._write_ppumask(value)

        # OAMADDR selects a byte
        if offset == 3:
            self._oam_address = value
            
        # OAMDATA writes advance and wrap the address.
        if offset == 4:
            self._oam[self._oam_address] = value
            self._oam_address = (self._oam_address + 1) & 0xFF

        # PPUADDR ($2006) selects the PPU video address in two writes.
        if offset == 6:
            self._write_ppuaddr(value)

        # PPUDATA ($2007) writes video memory and advances the selected address.
        if offset == 7:
            self._write_ppudata(value)


    def _write_ppuctrl(self, value):
        # Enabling NMI while vblank is set creates a new edge, even between frame boundaries.
        if self._vblank and not self._nmi_enabled and value & 0x80:
            self._nmi_pending = True

        # Decode VPHB SINN into independent settings; NN selects the base nametable coordinates.
        self._base_nametable_x = bool(value & 0x01)
        self._base_nametable_y = bool(value & 0x02)
        self._increment_32 = bool(value & 0x04)
        self._sprite_pattern_table_high = bool(value & 0x08)
        self._background_pattern_table_high = bool(value & 0x10)
        self._sprite_height_16 = bool(value & 0x20)
        self._ext_output_enabled = bool(value & 0x40)
        self._nmi_enabled = bool(value & 0x80)


    def _write_ppumask(self, value):
        self._background_enabled = bool(value & 0x08)
        self._sprites_enabled = bool(value & 0x10)


    def _read_ppustatus(self):
        # PPUSTATUS reports and clears vblank without changing the running frame phase.
        self._awaiting_second_write = False
        status = 0x80 if self._vblank else 0x00
        self._vblank = False
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


    def advance(self, cycles):
        """Advance the approximate video phase by completed CPU instruction cycles."""
        # Process each crossed frame separately so a large advance cannot skip vblank transitions.
        while cycles:
            elapsed = min(cycles, FRAME_CPU_CYCLES - self._frame_cycle)
            previous = self._frame_cycle
            self._frame_cycle += elapsed
            cycles -= elapsed

            # Vblank starts and clears at fixed CPU-cycle boundaries, independently of status reads.
            if previous < VBLANK_START_CPU_CYCLE <= self._frame_cycle:
                self._vblank = True
                if self._nmi_enabled:
                    self._nmi_pending = True
                logger.debug("Vblank started")
                if self._frame_output_enabled:
                    frame = self.render_frame()
                    tiles = bytes(self.read_vram(address) for address in range(0x2000, 0x23C0))
                    attributes = bytes(self.read_vram(address) for address in range(0x23C0, 0x2400))
                    colors = tuple(NES_COLORS[self.read_vram(0x3F00 + index)] for index in range(16))
                    self._published_frames += 1
                    self._completed_frame = (self._published_frames, frame)
                    self._completed_background = (self._published_frames, tiles, attributes, colors)
            if previous < VBLANK_END_CPU_CYCLE <= self._frame_cycle:
                self._vblank = False
                logger.debug("Vblank ended")
            if self._frame_cycle == FRAME_CPU_CYCLES:
                self._frame_cycle = 0


    def render_frame(self):
        """Render a native-size frame of packed RGB bytes."""
        # Start with the backdrop, including transparent background pattern pixels.
        colors = []
        for color_index in range(16):
            color_code = self.read_vram(0x3F00 + color_index)
            rgb = NES_COLORS[color_code]
            colors.append(rgb.to_bytes(3, "big"))

        # Fill the frame with backdrop color
        frame = bytearray(colors[0] * (256 * 240))
        if self._background_enabled:
            self._render_background(frame, colors)
        if self._sprites_enabled:
            self._render_sprites(frame)
        return bytes(frame)


    def _render_background(self, frame, colors):
        # The visible nametable contains 30 rows of 32 tiles, each covering 8x8 pixels.
        pattern_base = 0x1000 if self._background_pattern_table_high else 0
        for tile_y in range(30):
            for tile_x in range(32):
                # Each nametable byte selects one 16-byte tile in the chosen pattern table.
                tile = self.read_vram(0x2000 + tile_y * 32 + tile_x)

                # Each attribute byte covers 4x4 tiles; its four two-bit fields cover 2x2 tiles each.
                attribute_x = tile_x // 4
                attribute_y = tile_y // 4
                attribute_address = 0x23C0 + attribute_y * 8 + attribute_x
                attribute = self.read_vram(attribute_address)
                quadrant_x = (tile_x % 4) // 2
                quadrant_y = (tile_y % 4) // 2
                shift = quadrant_y * 4 + quadrant_x * 2
                palette = (attribute >> shift) & 0x03

                for row in range(8):
                    # The first eight bytes hold the low bitplane; the next eight hold the high bitplane.
                    address = pattern_base + tile * 16 + row
                    low = self.read_vram(address)
                    high = self.read_vram(address + 8)
                    for column in range(8):
                        # Bits run from left to right, most significant first; combine them into a 0-3 color index.
                        shift = 7 - column
                        color_index = ((high >> shift) & 1) * 2 + ((low >> shift) & 1)
                        if color_index:
                            # Each subpalette has four entries; index zero always leaves the backdrop visible.
                            palette_color_index = palette * 4 + color_index
                            # Convert tile and pixel coordinates to a linear pixel number in the 256-pixel-wide frame.
                            # Multiply by 3 because each pixel occupies three consecutive bytes: red, green, and blue.
                            offset = ((tile_y * 8 + row) * 256 + tile_x * 8 + column) * 3
                            frame[offset:offset + 3] = colors[palette_color_index]


    def _render_sprites(self, frame):
        # 8x16 pattern selection belongs to the next rendering step.
        if self._sprite_height_16:
            raise NotImplementedError("PPU 8x16 sprite rendering is not implemented")

        # PPUCTRL bit 3 selects the 4 KiB pattern table for all 8x8 sprites.
        pattern_base = 0x1000 if self._sprite_pattern_table_high else 0

        # Each of 64 OAM entries has four bytes: Y, tile number, attributes, and X.
        # Draw in reverse OAM order so earlier opaque sprites remain visible over later ones.
        for index in range(252, -1, -4):
            y, tile, attributes, x = self._oam[index:index + 4]

            # Attribute bits 0-1 select one of four sprite subpalettes; flips and priority are not yet applied.
            palette = attributes & 3

            # The sprite starts one scanline below OAM Y. Clip at the bottom; Y=$EF-$FF is entirely offscreen.
            for row in range(min(8, max(0, 239 - y))):
                # A tile occupies 16 CHR bytes: eight low bitplane rows followed by eight high bitplane rows.
                address = pattern_base + tile * 16 + row
                low = self.read_vram(address)
                high = self.read_vram(address + 8)

                # Clip columns at the right edge and combine the two bitplanes, most significant bit first.
                for column in range(min(8, 256 - x)):
                    shift = 7 - column
                    color_index = ((high >> shift) & 1) * 2 + ((low >> shift) & 1)
                    if color_index:
                        # Index zero is transparent; indices 1-3 select colors in the sprite palette at $3F10-$3F1F.
                        code = self.read_vram(0x3F10 + palette * 4 + color_index)

                        # Convert screen coordinates to the byte offset of a packed RGB pixel.
                        offset = ((y + 1 + row) * 256 + x + column) * 3
                        frame[offset:offset + 3] = NES_COLORS[code].to_bytes(3, "big")


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
