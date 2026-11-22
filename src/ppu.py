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
        self._background_left_enabled = False
        self._sprites_left_enabled = False
        self._grayscale_enabled = False
        self._color_emphasis = 0
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
        # The PPU's temporary register t is shared by scroll settings and PPUADDR writes.
        self._scroll_address_latch = 0
        self._fine_x = 0
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

        # PPUSCROLL shares the first/second write toggle and temporary address with PPUADDR.
        if offset == 5:
            self._write_ppuscroll(value)

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
        self._scroll_address_latch = (self._scroll_address_latch & ~0x0C00) | ((value & 0x03) << 10)
        self._increment_32 = bool(value & 0x04)
        self._sprite_pattern_table_high = bool(value & 0x08)
        self._background_pattern_table_high = bool(value & 0x10)
        self._sprite_height_16 = bool(value & 0x20)
        self._ext_output_enabled = bool(value & 0x40)
        self._nmi_enabled = bool(value & 0x80)


    def _write_ppumask(self, value):
        self._grayscale_enabled = bool(value & 0x01)
        self._background_left_enabled = bool(value & 0x02)
        self._sprites_left_enabled = bool(value & 0x04)
        self._background_enabled = bool(value & 0x08)
        self._sprites_enabled = bool(value & 0x10)
        self._color_emphasis = (value >> 5) & 0x07


    def _read_ppustatus(self):
        # PPUSTATUS reports and clears vblank without changing the running frame phase.
        self._awaiting_second_write = False
        status = 0x80 if self._vblank else 0x00
        self._vblank = False
        return status


    def _write_ppuscroll(self, value):
        # The 15-bit latch t has layout yyy NN YYYYY XXXXX: fine Y, nametable, coarse Y, and coarse X.
        # The first byte is a horizontal pixel offset: bits 7-3 select a tile and bits 2-0 a pixel within it.
        if not self._awaiting_second_write:
            # Clear t bits 0-4, then shift the five coarse X bits down into that field; preserve all other fields.
            self._scroll_address_latch = (self._scroll_address_latch & ~0x001F) | (value >> 3)

            # Fine X has its own 3-bit latch because t has no space for it.
            self._fine_x = value & 7
        else:
            # The second byte is a vertical pixel offset with the same coarse/fine split as the first byte.
            # Clear coarse Y (bits 5-9) and fine Y (bits 12-14), preserving nametable and coarse X fields.
            # Shift value bits 7-3 left by 2 into coarse Y; shift bits 2-0 left by 12 into fine Y.
            self._scroll_address_latch = (
                (self._scroll_address_latch & ~0x73E0) | ((value & 0xF8) << 2) | ((value & 7) << 12)
            )

        # $2005 and $2006 share this toggle; a $2002 read also resets it to the first-write state.
        self._awaiting_second_write = not self._awaiting_second_write


    def _write_ppuaddr(self, value):
        # The first write selects the upper six address bits; the second commits the full address.
        if not self._awaiting_second_write:
            self._scroll_address_latch = (self._scroll_address_latch & 0x00FF) | ((value & 0x3F) << 8)
        else:
            self._scroll_address_latch = (self._scroll_address_latch & 0x7F00) | value
            self._vram_address = self._scroll_address_latch
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
                    colors = tuple(self._render_color(0x3F00 + index) for index in range(16))
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
            rgb = self._render_color(0x3F00 + color_index)
            colors.append(rgb.to_bytes(3, "big"))

        # Fill the frame with backdrop color
        frame = bytearray(colors[0] * (256 * 240))
        background_opaque = bytearray(256 * 240)
        if self._background_enabled:
            self._render_background(frame, colors, background_opaque)
        if self._sprites_enabled:
            self._render_sprites(frame, background_opaque)
        return bytes(frame)


    def _render_background(self, frame, colors, background_opaque):
        # The temporary scroll state selects the frame origin in a 2x2 grid of logical nametables.
        address = self._scroll_address_latch
        scroll_x = ((address >> 10) & 1) * 256 + (address & 0x1F) * 8 + self._fine_x
        scroll_y = ((address >> 11) & 1) * 240 + ((address >> 5) & 0x1F) * 8 + ((address >> 12) & 7)
        pattern_base = 0x1000 if self._background_pattern_table_high else 0

        # Include partial tiles at the top and left, wrapping at each nametable boundary.
        for screen_y in range(-(scroll_y % 8), 240, 8):
            world_y = (scroll_y + screen_y) % 480
            tile_y = (world_y % 240) // 8
            for screen_x in range(-(scroll_x % 8), 256, 8):
                world_x = (scroll_x + screen_x) % 512
                tile_x = (world_x % 256) // 8
                nametable = 0x2000 + (world_y // 240 * 2 + world_x // 256) * 0x400

                # Attributes and tile bytes come from the same logical nametable, subject to cartridge mirroring.
                tile = self.read_vram(nametable + tile_y * 32 + tile_x)
                attribute = self.read_vram(nametable + 0x3C0 + tile_y // 4 * 8 + tile_x // 4)
                shift = (tile_y % 4 // 2) * 4 + (tile_x % 4 // 2) * 2
                palette = (attribute >> shift) & 3

                # Decode the two bitplanes and clip partial tiles to screen coordinates and the left mask.
                for row in range(8):
                    y = screen_y + row
                    if not 0 <= y < 240:
                        continue
                    pattern = pattern_base + tile * 16 + row
                    low = self.read_vram(pattern)
                    high = self.read_vram(pattern + 8)
                    for column in range(8):
                        x = screen_x + column
                        if not 0 <= x < 256 or (x < 8 and not self._background_left_enabled):
                            continue
                        shift = 7 - column
                        color_index = ((high >> shift) & 1) * 2 + ((low >> shift) & 1)
                        if color_index:
                            pixel = y * 256 + x
                            background_opaque[pixel] = 1
                            offset = pixel * 3
                            frame[offset:offset + 3] = colors[palette * 4 + color_index]


    def _render_sprites(self, frame, background_opaque):
        # PPUCTRL bit 5 selects a height of 8 or 16 pixels for every sprite.
        height = 16 if self._sprite_height_16 else 8

        # Select the first opaque sprite pixel in OAM order, even when the background hides it.
        sprite_selected = bytearray(256 * 240)
        for index in range(0, 256, 4):
            # Each of 64 OAM entries has four bytes: Y, tile number, attributes, and X.
            y, tile, attributes, x = self._oam[index:index + 4]

            # Attribute bits 0-1 select a sprite subpalette; bit 5 places the sprite behind opaque background.
            palette = attributes & 3

            # In 8x16 mode the tile's low bit selects the table; the remaining bits select an even tile pair.
            # In 8x8 mode PPUCTRL bit 3 selects the table and all eight tile bits select the tile.
            if self._sprite_height_16:
                pattern_base = (tile & 1) * 0x1000
                tile &= 0xFE
            else:
                pattern_base = 0x1000 if self._sprite_pattern_table_high else 0

            # The sprite starts one scanline below OAM Y. Clip at the bottom; Y=$EF-$FF is entirely offscreen.
            for row in range(min(height, max(0, 239 - y))):
                # A tile occupies 16 CHR bytes: eight low bitplane rows followed by eight high bitplane rows.
                # Rows 8-15 of an 8x16 sprite come from the next tile, starting again at its first row.
                address = pattern_base + (tile + row // 8) * 16 + row % 8
                low = self.read_vram(address)
                high = self.read_vram(address + 8)

                # Clip columns at the right edge and combine the two bitplanes, most significant bit first.
                for column in range(min(8, 256 - x)):
                    # A masked sprite pixel cannot claim a position or obscure another layer.
                    if x + column < 8 and not self._sprites_left_enabled:
                        continue
                    shift = 7 - column
                    color_index = ((high >> shift) & 1) * 2 + ((low >> shift) & 1)
                    if color_index:
                        # Transparent pixels do not claim a position; an earlier opaque sprite always wins it.
                        pixel = (y + 1 + row) * 256 + x + column
                        if sprite_selected[pixel]:
                            continue
                        sprite_selected[pixel] = 1

                        # A behind-background sprite is hidden only by a nonzero background pattern index.
                        if attributes & 0x20 and background_opaque[pixel]:
                            continue
                        offset = pixel * 3
                        color = self._render_color(0x3F10 + palette * 4 + color_index)
                        frame[offset:offset + 3] = color.to_bytes(3, "big")


    def _render_color(self, address):
        # Grayscale removes the hue bits when converting a palette entry to RGB, without changing palette RAM.
        code = self.read_vram(address)
        if self._grayscale_enabled:
            code &= 0x30
        rgb = NES_COLORS[code]

        # NTSC approximation: each emphasis bit attenuates the other two RGB channels by 3/4.
        channels = [(rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF]
        for emphasized in range(3):
            if self._color_emphasis & (1 << emphasized):
                for channel in range(3):
                    if channel != emphasized:
                        channels[channel] = channels[channel] * 3 // 4
        return (channels[0] << 16) | (channels[1] << 8) | channels[2]


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
