"""Verify PPU backdrop rendering from a synthetic CPU program."""

import pygame
import pytest

from frame_display import FrameDisplay
from machine import Machine
from nesfile import NESFile
from nes_palette import NES_COLORS


@pytest.mark.parametrize("height", [8, 16])
@pytest.mark.parametrize("flips", [0x00, 0x40, 0x80, 0xC0])
def test_sprite_flips_reverse_complete_asymmetric_pattern(tmp_path, height, flips):
    # Distinct points and colors in both halves expose horizontal, vertical, and combined reflections.
    points = {(0, 0): 1, (5, 1): 2, (2, 7): 3}
    if height == 16:
        points.update({(7, 8): 1, (4, 14): 2, (1, 15): 3})
    chr_rom = bytearray(8192)
    for (x, y), color in points.items():
        address = 0x1000 + (4 + y // 8) * 16 + y % 8
        if color & 1:
            chr_rom[address] |= 0x80 >> x
        if color & 2:
            chr_rom[address + 8] |= 0x80 >> x
    path = tmp_path / "flip.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    for address, code in ((0x3F00, 0x0F), (0x3F11, 0x01), (0x3F12, 0x21), (0x3F13, 0x30)):
        ppu.write_vram(address, code)
    machine.write_byte(0x2003, 0)
    for _ in range(64):
        for value in (0xFF, 0, 0, 0):
            machine.write_byte(0x2004, value)
    machine.write_byte(0x2003, 0)
    for value in (19, 4 if height == 8 else 5, flips, 30):
        machine.write_byte(0x2004, value)
    machine.write_byte(0x2000, 0x08 if height == 8 else 0x20)
    machine.write_byte(0x2001, 0x10)
    frame = ppu.render_frame()

    # Compare every pixel in the unchanged bounding box, including transparent pixels and the 8x16 tile seam.
    expected = {(7 - x if flips & 0x40 else x, height - 1 - y if flips & 0x80 else y): color
                for (x, y), color in points.items()}
    codes = (0x0F, 0x01, 0x21, 0x30)
    for y in range(height):
        for x in range(8):
            offset = ((20 + y) * 256 + 30 + x) * 3
            assert frame[offset:offset + 3] == NES_COLORS[codes[expected.get((x, y), 0)]].to_bytes(3, "big")


@pytest.mark.parametrize("height", [8, 16])
def test_flipped_sprite_clips_after_selecting_full_pattern(tmp_path, height):
    # The bottom-right source pixel becomes the top-left pixel even when most of the sprite is offscreen.
    chr_rom = bytearray(8192)
    chr_rom[(4 + (height - 1) // 8) * 16 + 7] = 0x01
    path = tmp_path / "flip-edge.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    machine.ppu.write_vram(0x3F00, 0x0F)
    machine.ppu.write_vram(0x3F11, 0x30)
    machine.write_byte(0x2003, 0)
    for _ in range(64):
        for value in (0xFF, 0, 0, 0):
            machine.write_byte(0x2004, value)
    machine.write_byte(0x2003, 0)
    for value in (236, 4, 0xC0, 253):
        machine.write_byte(0x2004, value)
    machine.write_byte(0x2000, 0x20 if height == 16 else 0)
    machine.write_byte(0x2001, 0x10)
    frame = machine.ppu.render_frame()

    # The point lands at (253, 237); the remaining visible and wrapped pixels are backdrop.
    offset = (237 * 256 + 253) * 3
    assert frame[offset:offset + 3] == bytes((255, 254, 255))
    assert frame[offset + 3:offset + 6] == bytes((0, 0, 0))
    assert frame[:3] == bytes((0, 0, 0))


def test_fine_scroll_moves_pattern_and_attribute_boundaries(tmp_path):
    # A recognizable tile row and two attribute quadrants expose sub-tile scrolling.
    chr_rom = bytearray(8192)
    chr_rom[16 + 5] = 0xFF
    path = tmp_path / "fine-scroll.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    for tile_x in range(4):
        ppu.write_vram(0x2000 + tile_x, 1)
    ppu.write_vram(0x23C0, 0x04)
    ppu.write_vram(0x3F01, 0x01)
    ppu.write_vram(0x3F05, 0x21)
    machine.write_byte(0x2005, 3)
    machine.write_byte(0x2005, 5)
    machine.write_byte(0x2001, 0x0A)
    frame = ppu.render_frame()

    # World x=16 appears at screen x=13; world row 5 appears at screen row 0.
    assert frame[12 * 3:13 * 3] == bytes((0, 42, 136))
    assert frame[13 * 3:14 * 3] == bytes((100, 176, 255))
    assert frame[(256 + 13) * 3:(256 + 14) * 3] == bytes((102, 102, 102))


@pytest.mark.parametrize("mirroring,physical_pages", [(0, (0, 0, 1, 1)), (1, (0, 1, 0, 1))])
@pytest.mark.parametrize("base", [0, 1, 2, 3])
def test_scroll_crosses_both_nametable_boundaries(tmp_path, mirroring, physical_pages, base):
    # Fill each physical nametable with its own opaque tile and set a distinct color for each tile.
    chr_rom = bytearray(8192)
    chr_rom[16:24] = bytes([0xFF] * 8)
    chr_rom[40:48] = bytes([0xFF] * 8)
    path = tmp_path / "scroll.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1, mirroring]) + bytes(9) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    for logical, page in enumerate(physical_pages):
        for offset in range(960):
            ppu.write_vram(0x2000 + logical * 0x400 + offset, page + 1)
    ppu.write_vram(0x3F01, 0x01)
    ppu.write_vram(0x3F02, 0x21)

    # Scroll five pixels before both edges, with the entire left edge enabled.
    machine.write_byte(0x2000, base)
    machine.write_byte(0x2005, 251)
    machine.write_byte(0x2005, 235)
    machine.write_byte(0x2001, 0x0A)
    frame = ppu.render_frame()
    logical = (base, base ^ 1, base ^ 2, base ^ 3)
    colors = ((0, 42, 136), (100, 176, 255))
    for (x, y), table in zip(((4, 4), (5, 4), (4, 5), (5, 5)), logical):
        offset = (y * 256 + x) * 3
        assert tuple(frame[offset:offset + 3]) == colors[physical_pages[table]]

    # The left mask stays anchored to the screen rather than moving with the scrolled tiles.
    machine.write_byte(0x2001, 0x08)
    frame = ppu.render_frame()
    assert frame[(5 * 256 + 7) * 3:(5 * 256 + 8) * 3] == bytes((102, 102, 102))
    assert tuple(frame[(5 * 256 + 8) * 3:(5 * 256 + 9) * 3]) == colors[physical_pages[base ^ 3]]


@pytest.mark.parametrize("mask,rgb", [
    (0x00, (21, 95, 217)), (0x20, (21, 71, 162)), (0x40, (15, 95, 162)), (0x80, (15, 71, 217)),
    (0x60, (15, 71, 121)), (0xA0, (15, 53, 162)), (0xC0, (11, 71, 162)), (0xE0, (11, 53, 121)),
])
def test_ntsc_color_emphasis_combinations_on_backdrop(make_cpu, mask, rgb):
    # All channels are nonzero and reveal repeated integer attenuation for combined bits.
    _, machine = make_cpu()
    machine.ppu.write_vram(0x3F00, 0x11)
    machine.write_byte(0x2009, mask)
    assert machine.ppu.render_frame() == bytes(rgb) * (256 * 240)
    assert machine.ppu.read_vram(0x3F00) == 0x11


def test_grayscale_and_emphasis_apply_to_both_layers_and_backdrop(tmp_path):
    # Distinct non-gray codes supply the backdrop, a background pixel, and a separate sprite pixel.
    chr_rom = bytearray(8192)
    chr_rom[16] = 0x80
    path = tmp_path / "emphasis.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    ppu.write_vram(0x2042, 1)
    for address, code in ((0x3F00, 0x06), (0x3F01, 0x16), (0x3F11, 0x26)):
        ppu.write_vram(address, code)
    machine.write_byte(0x2003, 0)
    for _ in range(64):
        for value in (0xFF, 0, 0, 0):
            machine.write_byte(0x2004, value)
    machine.write_byte(0x2003, 0)
    for value in (15, 1, 0, 32):
        machine.write_byte(0x2004, value)

    # Grayscale selects $00, $10, and $20 before red emphasis attenuates green and blue.
    machine.write_byte(0x2001, 0x39)
    frame = ppu.render_frame()
    for x, expected in ((16, (173, 129, 129)), (32, (255, 190, 191)), (40, (102, 76, 76))):
        offset = (16 * 256 + x) * 3
        assert frame[offset:offset + 3] == bytes(expected)
    assert [ppu.read_vram(address) for address in (0x3F00, 0x3F01, 0x3F11)] == [0x06, 0x16, 0x26]


@pytest.mark.parametrize("code", [0x0F, 0x16, 0x21, 0x3D])
def test_grayscale_masks_backdrop_color_without_changing_palette(make_cpu, code):
    # Render each brightness range with grayscale off, on, then off again.
    _, machine = make_cpu()
    ppu = machine.ppu
    ppu.write_vram(0x3F00, code)
    for mask, expected in ((0, code), (1, code & 0x30), (0, code)):
        machine.write_byte(0x2009, mask)
        assert ppu.render_frame() == NES_COLORS[expected].to_bytes(3, "big") * (256 * 240)
        assert ppu.read_vram(0x3F00) == code

    # Palette reads through the existing PPUDATA model continue returning the unmasked stored byte.
    machine.write_byte(0x2001, 1)
    machine.write_byte(0x2006, 0x3F)
    machine.write_byte(0x2006, 0)
    assert machine.read_byte(0x2007) == code


def test_grayscale_applies_to_background_and_sprite_pixels(tmp_path):
    # Place separate opaque background and sprite pixels with different palette color codes.
    chr_rom = bytearray(8192)
    chr_rom[16] = 0x80
    path = tmp_path / "grayscale.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    ppu.write_vram(0x2042, 1)
    for address, code in ((0x3F00, 0x0F), (0x3F01, 0x16), (0x3F11, 0x21)):
        ppu.write_vram(address, code)
    machine.write_byte(0x2003, 0)
    for _ in range(64):
        for value in (0xFF, 0, 0, 0):
            machine.write_byte(0x2004, value)
    machine.write_byte(0x2003, 0)
    for value in (15, 1, 0, 32):
        machine.write_byte(0x2004, value)

    # Grayscale changes output colors for both layers and the backdrop, without changing palette data.
    for mask, codes in ((0x18, (0x0F, 0x16, 0x21)), (0x19, (0x00, 0x10, 0x20))):
        machine.write_byte(0x2001, mask)
        frame = ppu.render_frame()
        for x, code in zip((40, 16, 32), codes):
            offset = (16 * 256 + x) * 3
            assert frame[offset:offset + 3] == NES_COLORS[code].to_bytes(3, "big")
    assert [ppu.read_vram(address) for address in (0x3F00, 0x3F01, 0x3F11)] == [0x0F, 0x16, 0x21]


@pytest.mark.parametrize("layers", [0x00, 0x08, 0x10, 0x18])
@pytest.mark.parametrize("edges", [0x00, 0x02, 0x04, 0x06])
def test_left_edge_masks_independently_clip_layers(tmp_path, layers, edges):
    # Fill the first two background tiles and two behind-background sprites with opaque pixels.
    chr_rom = bytearray(8192)
    chr_rom[16:24] = bytes([0xFF] * 8)
    path = tmp_path / "left-edge.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    ppu.write_vram(0x2020, 1)
    ppu.write_vram(0x2021, 1)
    for address, color in ((0x3F00, 0x0F), (0x3F01, 0x01), (0x3F11, 0x21)):
        ppu.write_vram(address, color)
    machine.write_byte(0x2003, 0)
    for _ in range(64):
        for value in (0xFF, 0, 0, 0):
            machine.write_byte(0x2004, value)
    machine.write_byte(0x2003, 0)
    for value in (7, 1, 0x20, 0, 7, 1, 0x20, 8):
        machine.write_byte(0x2004, value)

    # Test every combination through a mirrored PPUMASK port, including the first unmasked column.
    machine.write_byte(0x2009, layers | edges)
    frame = ppu.render_frame()
    backdrop, background, sprite = (0, 0, 0), (0, 42, 136), (100, 176, 255)
    left = background if layers & 0x08 and edges & 0x02 else sprite if layers & 0x10 and edges & 0x04 else backdrop
    right = background if layers & 0x08 else sprite if layers & 0x10 else backdrop
    pixels = [tuple(frame[(8 * 256 + x) * 3:(8 * 256 + x) * 3 + 3]) for x in range(9)]
    assert pixels == [left] * 8 + [right]


def test_sprite_background_priority_and_layer_combinations(tmp_path):
    # The background has opaque pixels at columns 0 and 2; the first has the same color as the backdrop.
    chr_rom = bytearray(8192)
    chr_rom[16] = 0x80
    chr_rom[24] = 0x20
    chr_rom[32] = 0xE0
    chr_rom[48:56] = bytes([0xF0] * 8)
    path = tmp_path / "priority.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    ppu.write_vram(0x2000 + 2 * 32 + 2, 1)
    for address, color in ((0x3F00, 0x0F), (0x3F01, 0x0F), (0x3F02, 0x30),
                           (0x3F11, 0x01), (0x3F15, 0x21)):
        ppu.write_vram(address, color)

    # The first sprite is behind the background; the second is in front and has a different color.
    machine.write_byte(0x2003, 0)
    for _ in range(64):
        for value in (0xFF, 0, 0, 0):
            machine.write_byte(0x2004, value)
    machine.write_byte(0x2003, 0)
    for value in (15, 2, 0x20, 16, 15, 3, 1, 16):
        machine.write_byte(0x2004, value)

    # The first opaque sprite claims a pixel before its background priority is considered.
    black, white, first, second = (0, 0, 0), (255, 254, 255), (0, 42, 136), (100, 176, 255)
    expected = {
        0x00: [black, black, black, black],
        0x08: [black, black, white, black],
        0x10: [first, first, first, second],
        0x18: [black, first, white, second],
    }
    for mask, colors in expected.items():
        machine.write_byte(0x2001, mask)
        frame = ppu.render_frame()
        pixels = [tuple(frame[(16 * 256 + x) * 3:(16 * 256 + x) * 3 + 3]) for x in range(16, 20)]
        assert pixels == colors

    # With front priority, the first sprite covers even an opaque background pixel of the same backdrop color.
    machine.write_byte(0x2003, 2)
    machine.write_byte(0x2004, 0)
    frame = ppu.render_frame()
    assert tuple(frame[(16 * 256 + 16) * 3:(16 * 256 + 16) * 3 + 3]) == first
    assert tuple(frame[(16 * 256 + 18) * 3:(16 * 256 + 18) * 3 + 3]) == first


def test_8x8_sprites_use_oam_position_pattern_table_and_palette(tmp_path):
    # Give tile 1 asymmetric bitplanes in both pattern tables and hide unused OAM entries.
    chr_rom = bytearray(8192)
    chr_rom[16] = 0xA0
    chr_rom[24] = 0x60
    chr_rom[0x1011] = 0x40
    chr_rom[0x1019] = 0x80
    chr_rom[32:40] = bytes([0xFF] * 8)
    path = tmp_path / "sprites.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    machine.write_byte(0x2003, 0)
    for _ in range(64):
        for value in (0xFF, 0, 0, 0):
            machine.write_byte(0x2004, value)
    machine.write_byte(0x2003, 0)
    for value in (19, 1, 2, 30):
        machine.write_byte(0x2004, value)
    for address, code in ((0x3F00, 0x0F), (0x3F19, 0x01), (0x3F1A, 0x21), (0x3F1B, 0x30)):
        ppu.write_vram(address, code)

    def pixel(frame, x, y):
        offset = (y * 256 + x) * 3
        return tuple(frame[offset:offset + 3])

    # Sprite Y is one line above its first pixel; index zero leaves the backdrop intact.
    black, first, second, third = (0, 0, 0), (0, 42, 136), (100, 176, 255), (255, 254, 255)
    assert pixel(ppu.render_frame(), 30, 20) == black
    machine.write_byte(0x2001, 0x10)
    frame = ppu.render_frame()
    assert [pixel(frame, x, 20) for x in range(30, 34)] == [first, second, third, black]
    assert pixel(frame, 30, 19) == black
    assert pixel(frame, 29, 20) == black

    # Transparent sprite pixels preserve an opaque background pixel.
    ppu.write_vram(0x2000 + 2 * 32 + 4, 2)
    ppu.write_vram(0x3F01, 0x21)
    machine.write_byte(0x2001, 0x18)
    assert pixel(ppu.render_frame(), 33, 20) == second

    # PPUCTRL bit 3 selects the second pattern table for 8x8 sprites.
    machine.write_byte(0x2001, 0x10)
    machine.write_byte(0x2000, 0x08)
    frame = ppu.render_frame()
    assert [pixel(frame, x, 21) for x in range(30, 33)] == [second, first, black]
    assert pixel(frame, 30, 20) == black


def test_8x8_sprites_clip_at_screen_edges_and_do_not_wrap_y(tmp_path):
    # The opaque tile reaches the lower-right corner; hidden sprites must not wrap to the first line.
    chr_rom = bytearray(8192)
    chr_rom[16:24] = bytes([0xFF] * 8)
    path = tmp_path / "edge.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    machine.write_byte(0x2003, 0)
    for _ in range(64):
        for value in (0xFF, 1, 0, 255):
            machine.write_byte(0x2004, value)
    machine.write_byte(0x2003, 0)
    machine.write_byte(0x2004, 238)
    machine.ppu.write_vram(0x3F00, 0x0F)
    machine.ppu.write_vram(0x3F11, 0x30)
    machine.write_byte(0x2001, 0x10)
    frame = machine.ppu.render_frame()
    assert frame[0:3] == bytes((0, 0, 0))
    assert frame[-3:] == bytes((255, 254, 255))
    assert frame[-6:-3] == bytes((0, 0, 0))


@pytest.mark.parametrize("tile,control", [(0x04, 0x20), (0x04, 0x28), (0x05, 0x20), (0x05, 0x28)])
def test_8x16_sprites_select_table_and_ordered_tile_pair(tmp_path, tile, control):
    # Distinct pixels at both ends of each tile expose the table, tile order, and row boundaries.
    chr_rom = bytearray(8192)
    chr_rom[0x0040] = 0x80
    chr_rom[0x0047] = 0x40
    chr_rom[0x0058] = 0x20
    chr_rom[0x005F] = 0x10
    chr_rom[0x1048] = 0x80
    chr_rom[0x104F] = 0x40
    chr_rom[0x1050] = 0x20
    chr_rom[0x1057] = 0x10
    path = tmp_path / "tall-sprite.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    machine.write_byte(0x2003, 0)
    for _ in range(64):
        for value in (0xFF, 0, 0, 0):
            machine.write_byte(0x2004, value)
    machine.write_byte(0x2003, 0)
    for value in (19, tile, 0, 30):
        machine.write_byte(0x2004, value)
    for address, color in ((0x3F00, 0x0F), (0x3F11, 0x01), (0x3F12, 0x21)):
        machine.ppu.write_vram(address, color)
    machine.write_byte(0x2000, control)
    machine.write_byte(0x2001, 0x10)
    frame = machine.ppu.render_frame()

    # Bit 0 of the OAM tile selects the table, independently of PPUCTRL bit 3.
    def pixel(x, y):
        offset = (y * 256 + x) * 3
        return tuple(frame[offset:offset + 3])

    black, first, second = (0, 0, 0), (0, 42, 136), (100, 176, 255)
    top, bottom = (first, second) if tile == 0x04 else (second, first)
    assert [pixel(x, y) for x, y in ((30, 20), (31, 27), (32, 28), (33, 35))] == [top, top, bottom, bottom]
    assert pixel(30, 19) == black
    assert pixel(33, 36) == black
    assert pixel(31, 20) == black

    # The bottom tile can begin on the last visible scanline without wrapping the remaining rows.
    machine.write_byte(0x2003, 0)
    machine.write_byte(0x2004, 230)
    frame = machine.ppu.render_frame()
    assert pixel(31, 238) == top
    assert pixel(32, 239) == bottom
    assert pixel(32, 0) == black


@pytest.fixture
def display(monkeypatch):
    # The dummy driver lets the presenter expose its scaled pixels without opening a desktop window.
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    pygame.display.quit()
    presenter = FrameDisplay()
    yield presenter
    pygame.display.quit()


@pytest.mark.parametrize("color,rgb", [
    (0x00, (102, 102, 102)),
    (0x01, (0, 42, 136)),
    (0x21, (100, 176, 255)),
    (0x30, (255, 254, 255)),
    (0xE1, (100, 176, 255)),
])
def test_cpu_palette_write_renders_and_presents_backdrop(make_cpu, display, color, rgb):
    # The CPU writes a backdrop color through the PPU's memory-mapped registers.
    program = bytes([
        0xA9,  # LDA #$00: Load zero for PPUMASK.
        0x00,
        0x8D,  # STA $2001: Disable both layers.
        0x01,
        0x20,
        0xA9,  # LDA #$3F: Load the high byte of palette address $3F00.
        0x3F,
        0x8D,  # STA $2006: Set the high byte through PPUADDR.
        0x06,
        0x20,
        0xA9,  # LDA #$00: Load the low byte of palette address $3F00.
        0x00,
        0x8D,  # STA $2006: Set the low byte and select $3F00.
        0x06,
        0x20,
        0xA9,  # LDA #color: Load the test's NES color code.
        color,
        0x8D,  # STA $2007: Write the backdrop color through PPUDATA.
        0x07,
        0x20,
    ])
    cpu, machine = make_cpu(start_address=0x8000, prg_program=program)
    for _ in range(8):
        cpu.step()

    # The native frame uses $3F00 even though the data write advanced the address to $3F01.
    assert machine.ppu.read_vram(0x3F00) == color & 0x3F
    assert machine.ppu._vram_address == 0x3F01
    frame = machine.ppu.render_frame()
    assert frame == bytes(rgb) * (256 * 240)

    # Present the same packed bytes and verify every pixel in the 3× display surface.
    display.present(frame)
    screen = pygame.display.get_surface()
    assert screen.get_size() == (768, 720)
    assert pygame.image.tobytes(screen, "RGB") == bytes(rgb) * (768 * 720)


def test_stationary_background_pattern_tables_and_transparency(tmp_path):
    # Tile 1 has different asymmetric bitplanes in the two pattern tables.
    chr_rom = bytearray(8192)
    chr_rom[16] = 0xA0
    chr_rom[24] = 0x60
    chr_rom[0x1010 + 1] = 0x40
    chr_rom[0x1018 + 1] = 0x80
    prg = bytearray(16384)
    path = tmp_path / "background.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + prg + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    for index, code in enumerate((0x0F, 0x01, 0x21, 0x30)):
        ppu.write_vram(0x3F00 + index, code)
    ppu.write_vram(0x2000 + 32 + 2, 1)

    def pixel(frame, x, y):
        offset = (y * 256 + x) * 3
        return tuple(frame[offset:offset + 3])

    # Disabled output is all backdrop; enabled output decodes both planes and transparent zero.
    backdrop, first, second, third = (0, 0, 0), (0, 42, 136), (100, 176, 255), (255, 254, 255)
    assert pixel(ppu.render_frame(), 16, 8) == backdrop
    machine.write_byte(0x2009, 0x08)
    frame = ppu.render_frame()
    assert [pixel(frame, x, 8) for x in range(16, 20)] == [first, second, third, backdrop]
    assert pixel(frame, 16, 9) == backdrop
    assert pixel(frame, 15, 8) == backdrop

    # PPUCTRL bit 4 chooses the other table without changing nametable contents.
    machine.write_byte(0x2000, 0x10)
    frame = ppu.render_frame()
    assert [pixel(frame, x, 9) for x in range(16, 19)] == [second, first, backdrop]
    assert pixel(frame, 16, 8) == backdrop

    # A later mirrored PPUMASK write can disable the background again.
    machine.write_byte(0x3FF9, 0x16)
    assert pixel(ppu.render_frame(), 16, 9) == backdrop


def test_attribute_quadrants_select_background_subpalettes(tmp_path):
    # Every tile has seven opaque pixels and one transparent pixel per row.
    chr_rom = bytearray(8192)
    for row in range(8):
        chr_rom[row] = 0xFE
    path = tmp_path / "attributes.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    ppu.write_vram(0x3F00, 0x0F)
    for palette, color in enumerate((0x01, 0x21, 0x30, 0x00)):
        ppu.write_vram(0x3F01 + palette * 4, color)

    # The four quadrants select palettes 0, 1, 2, and 3 in reading order.
    ppu.write_vram(0x23C0, 0xE4)
    ppu.write_vram(0x23C1, 0x03)
    ppu.write_vram(0x23FF, 0x08)
    machine.write_byte(0x2001, 0x08)
    frame = ppu.render_frame()

    def pixel(x, y):
        offset = (y * 256 + x) * 3
        return tuple(frame[offset:offset + 3])

    # Check both sides of quadrant and attribute-byte boundaries, including the last visible tile row.
    assert pixel(14, 15) == (0, 42, 136)
    assert pixel(16, 15) == (100, 176, 255)
    assert pixel(14, 16) == (255, 254, 255)
    assert pixel(16, 16) == (102, 102, 102)
    assert pixel(30, 0) == (100, 176, 255)
    assert pixel(32, 0) == (102, 102, 102)
    assert pixel(240, 239) == (255, 254, 255)

    # Transparent pixels use the universal backdrop even in a nonzero subpalette.
    assert pixel(23, 16) == (0, 0, 0)
