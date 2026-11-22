"""Render a captured stationary background as tile numbers and palette swatches."""


# Each row stores a 3-pixel glyph from left to right in its three low bits.
HEX_GLYPHS = (
    (7, 5, 5, 5, 5, 5, 7),  # 0
    (2, 6, 2, 2, 2, 2, 7),  # 1
    (7, 1, 1, 7, 4, 4, 7),  # 2
    (7, 1, 1, 7, 1, 1, 7),  # 3
    (5, 5, 5, 7, 1, 1, 1),  # 4
    (7, 4, 4, 7, 1, 1, 7),  # 5
    (7, 4, 4, 7, 5, 5, 7),  # 6
    (7, 1, 1, 2, 2, 2, 2),  # 7
    (7, 5, 5, 7, 5, 5, 7),  # 8
    (7, 5, 5, 7, 1, 1, 7),  # 9
    (2, 5, 5, 7, 5, 5, 5),  # A
    (6, 5, 5, 6, 5, 5, 6),  # B
    (7, 4, 4, 4, 4, 4, 7),  # C
    (6, 5, 5, 5, 5, 5, 6),  # D
    (7, 4, 4, 6, 4, 4, 7),  # E
    (7, 4, 4, 6, 4, 4, 4),  # F
)


def render_background_inspection(snapshot):
    """Render a completed background snapshot as a 256 by 240 packed RGB frame."""
    # Black supplies the glyph background and the two empty columns in each tile.
    _, tiles, attributes, colors = snapshot
    frame = bytearray(256 * 240 * 3)
    rgb = tuple(color.to_bytes(3, "big") for color in colors)

    for tile_y in range(30):
        for tile_x in range(32):
            # Draw the two hex digits using native pixels, with one empty column after each digit.
            tile = tiles[tile_y * 32 + tile_x]
            for digit, value in enumerate((tile >> 4, tile & 0x0F)):
                for row, bits in enumerate(HEX_GLYPHS[value]):
                    for column in range(3):
                        if bits & (4 >> column):
                            offset = ((tile_y * 8 + row) * 256 + tile_x * 8 + digit * 4 + column) * 3
                            frame[offset:offset + 3] = b"\xff\xff\xff"

            # Attribute quadrants select a subpalette for each 2 by 2 tile region.
            attribute = attributes[(tile_y // 4) * 8 + tile_x // 4]
            shift = ((tile_y % 4) // 2) * 4 + ((tile_x % 4) // 2) * 2
            palette = (attribute >> shift) & 3
            for color_index in range(4):
                # Pattern index zero always uses the universal backdrop, regardless of the selected subpalette.
                color = rgb[palette * 4 + color_index if color_index else 0]
                offset = ((tile_y * 8 + 7) * 256 + tile_x * 8 + color_index * 2) * 3
                frame[offset:offset + 6] = color * 2

    return bytes(frame)
