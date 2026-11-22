"""Verify tile numbers and effective palette colors in captured background views."""

from background_inspection import render_background_inspection
from nes_palette import NES_COLORS


def pixel(frame, x, y):
    offset = (y * 256 + x) * 3
    return tuple(frame[offset:offset + 3])


def test_all_hex_digits_have_distinct_visible_glyphs():
    # Put every hexadecimal digit in the low position against the same leading zero.
    tiles = bytes(range(16)) + bytes(944)
    frame = render_background_inspection((1, tiles, bytes(64), (0,) * 16))
    glyphs = []
    for tile_x in range(16):
        glyph = tuple(pixel(frame, tile_x * 8 + 4 + x, y) for y in range(7) for x in range(3))
        assert (255, 255, 255) in glyph
        glyphs.append(glyph)
    assert len(set(glyphs)) == 16


def test_tile_digits_and_boundaries_with_background_disabled(make_cpu):
    # Capture two distinct tile numbers while the PPU background layer is disabled.
    _, machine = make_cpu()
    ppu = machine.ppu
    ppu.write_vram(0x2000, 0x0A)
    ppu.write_vram(0x23BF, 0xF5)
    ppu.enable_frame_output()
    ppu.advance(27394)
    snapshot = ppu.completed_background

    # Later VRAM changes must not affect the rendered snapshot.
    ppu.write_vram(0x2000, 0xFF)
    frame = render_background_inspection(snapshot)
    assert len(frame) == 256 * 240 * 3
    white = (255, 255, 255)
    black = (0, 0, 0)
    expected_first = ("###..#..", "#.#.#.#.", "#.#.#.#.", "#.#.###.",
                      "#.#.#.#.", "#.#.#.#.", "###.#.#.")
    expected_last = ("###.###.", "#...#...", "#...#...", "##..###.",
                     "#.....#.", "#.....#.", "#...###.")
    for row in range(7):
        assert [pixel(frame, x, row) for x in range(8)] == [white if c == "#" else black
                                                           for c in expected_first[row]]
        assert [pixel(frame, 248 + x, 232 + row) for x in range(8)] == [white if c == "#" else black
                                                                       for c in expected_last[row]]


def test_swatches_follow_attribute_quadrants_and_universal_backdrop(make_cpu):
    # Give each subpalette distinct colors and misleading values at its unused zero slot.
    _, machine = make_cpu()
    ppu = machine.ppu
    codes = (0x0F, 0x01, 0x02, 0x03, 0x30, 0x11, 0x12, 0x13,
             0x21, 0x15, 0x16, 0x17, 0x20, 0x25, 0x26, 0x27)
    for index, code in enumerate(codes):
        ppu.write_vram(0x3F00 + index, code)
    ppu.write_vram(0x23C0, 0xE4)
    ppu.write_vram(0x23FF, 0x0C)
    ppu.enable_frame_output()
    ppu.advance(27394)
    frame = render_background_inspection(ppu.completed_background)

    # Inspect both sides of each quadrant boundary and the bottom-right frame cell.
    for tile_x, tile_y, palette in ((1, 1, 0), (2, 1, 1), (1, 2, 2), (2, 2, 3), (31, 29, 3)):
        expected = [NES_COLORS[codes[0]]] + [NES_COLORS[codes[palette * 4 + i]] for i in range(1, 4)]
        swatches = [color.to_bytes(3, "big") for color in expected for _ in range(2)]
        assert [bytes(pixel(frame, tile_x * 8 + x, tile_y * 8 + 7)) for x in range(8)] == swatches
