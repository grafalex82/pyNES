"""Decode and compose CHR tiles for a future offline PNG exporter."""

import pygame


def decode_tile(tile):
    """Decode one 16-byte CHR tile into an 8-by-8 list of palette indices.

    The input contains eight low-bitplane row bytes followed by eight high-bitplane row bytes.
    The result is a list of rows from top to bottom; each row contains eight indices from left to right.
    Indices range from 0 to 3 and represent palette entries, not RGB colors.
    """
    # Each row uses corresponding bytes in the low and high bitplanes, with bit 7 at the left.
    pixels = []
    for row in range(8):
        low = tile[row]
        high = tile[row + 8]
        pixels.append([((low >> bit) & 1) | (((high >> bit) & 1) << 1) for bit in range(7, -1, -1)])
    return pixels


def render_chr_sheets(chr_rom, palettes, scale=1):
    """Render 8 KiB of CHR data into two off-screen pygame surfaces.

    The input contains two consecutive 4 KiB tile sheets. Palettes supplies four RGB colors per sheet, ordered by
    pixel index. Scale is 1 or 2 and affects tile pixels only. The returned surfaces are in CHR file order.
    """
    # A complete sheet pair avoids silently discarding data or inventing tiles.
    if len(chr_rom) != 8192:
        raise ValueError(f"Expected 8192 bytes of CHR ROM, got {len(chr_rom)}")
    if scale not in (1, 2):
        raise ValueError(f"Scale must be 1 or 2, got {scale}")

    # Separate the scaled tiles by one transparent output pixel, not one scaled pixel.
    tile_size = 8 * scale
    stride = tile_size + 1
    size = 16 * tile_size + 15
    sheets = []
    for sheet_index in range(2):
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        surface.fill((0, 0, 0, 0))

        # Tile and row order follow their storage order in the corresponding CHR half.
        for tile_index in range(256):
            start = sheet_index * 4096 + tile_index * 16
            x = (tile_index % 16) * stride
            y = (tile_index // 16) * stride
            for row, pixels in enumerate(decode_tile(chr_rom[start:start + 16])):
                for column, pixel in enumerate(pixels):
                    surface.fill(palettes[sheet_index][pixel], (x + column * scale, y + row * scale, scale, scale))

        # Coordinate parity produces one-pixel gray dots and transparent gaps, including at intersections.
        for boundary in range(1, 16):
            gutter = boundary * stride - 1
            for position in range(size):
                if (gutter + position) % 2 == 0:
                    surface.set_at((gutter, position), (128, 128, 128, 255))
                    surface.set_at((position, gutter), (128, 128, 128, 255))
        sheets.append(surface)
    return tuple(sheets)
