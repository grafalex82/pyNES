"""Verify CHR tile decoding and sheet composition with synthetic bitplanes."""

import pygame
import pytest

from misc.chr2png import decode_tile, render_chr_sheets


def test_decodes_both_bitplanes_in_row_and_pixel_order():
    # Asymmetric rows distinguish both bitplanes, left and right edges, and top and bottom rows.
    tile = bytes([
        0x93, 0x24, 0x00, 0xFF, 0x01, 0x40, 0x5A, 0x00,
        0x39, 0x80, 0xFF, 0x00, 0x80, 0x40, 0xA5, 0x01,
    ])

    # Values are palette indices, not colors; 3 requires a set bit in both planes.
    assert decode_tile(tile) == [
        [1, 0, 2, 3, 2, 0, 1, 3],
        [2, 0, 1, 0, 0, 1, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 0, 0, 0, 0, 0, 0, 1],
        [0, 3, 0, 0, 0, 0, 0, 0],
        [2, 1, 2, 1, 1, 2, 1, 2],
        [0, 0, 0, 0, 0, 0, 0, 2],
    ]


@pytest.mark.parametrize("scale,size", [(1, 143), (2, 271)])
def test_renders_both_sheets_with_unscaled_dotted_gutters(scale, size, monkeypatch):
    # Solid tiles cycle through four indices; the two sheet palettes make a swapped half visible.
    tiles = [bytes([255 if index & 1 else 0] * 8 + [255 if index & 2 else 0] * 8) for index in range(4)]
    chr_rom = b"".join(tiles[(tile + sheet) % 4] for sheet in range(2) for tile in range(256))
    palettes = (
        ((0, 0, 0), (10, 20, 30), (40, 50, 60), (70, 80, 90)),
        ((1, 2, 3), (11, 21, 31), (41, 51, 61), (71, 81, 91)),
    )
    monkeypatch.setattr(pygame.display, "set_mode", lambda *args, **kwargs: pytest.fail("display opened"))

    # Each source pixel is repeated exactly scale-by-scale without altering the one-pixel gaps.
    sheets = render_chr_sheets(chr_rom, palettes, scale)
    assert len(sheets) == 2
    tile_size = 8 * scale
    stride = tile_size + 1
    for sheet_index, surface in enumerate(sheets):
        assert surface.get_size() == (size, size)
        for tile in range(256):
            x = (tile % 16) * stride
            y = (tile // 16) * stride
            expected = (*palettes[sheet_index][(tile + sheet_index) % 4], 255)
            for dy in range(tile_size):
                for dx in range(tile_size):
                    assert surface.get_at((x + dx, y + dy)) == expected

        # Examine every separator pixel, including crossings and both ends of each gutter.
        for boundary in range(1, 16):
            gutter = boundary * stride - 1
            for position in range(size):
                expected = (128, 128, 128, 255) if (gutter + position) % 2 == 0 else (0, 0, 0, 0)
                assert surface.get_at((gutter, position)) == expected
                assert surface.get_at((position, gutter)) == expected


@pytest.mark.parametrize("scale", [1, 2])
def test_renders_asymmetric_first_and_last_tiles_in_both_sheets(scale):
    # Distinct corner pixels expose reversed halves, tile order, and horizontal or vertical flipping.
    chr_rom = bytearray(8192)
    chr_rom[0] = 0x80
    chr_rom[8] = 0x40
    chr_rom[4095] = 0x01
    chr_rom[4096] = 0x40
    chr_rom[4096 + 8] = 0x80
    chr_rom[8192 - 16 + 7] = 0x01
    palette = ((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255))
    sheets = render_chr_sheets(chr_rom, (palette, palette), scale)

    # Inspect the complete source pixel blocks, including the four outer sheet corners.
    size = 128 * scale + 15
    positions = ((0, 0), (scale, 0), (size - scale, size - scale))
    for surface, indices in zip(sheets, ((1, 2, 2), (2, 1, 1))):
        for (x, y), index in zip(positions, indices):
            for dy in range(scale):
                for dx in range(scale):
                    assert surface.get_at((x + dx, y + dy)) == (*palette[index], 255)


@pytest.mark.parametrize("size", [0, 16384])
def test_rejects_unsupported_chr_sizes(size):
    with pytest.raises(ValueError, match=f"Expected 8192 bytes of CHR ROM, got {size}"):
        render_chr_sheets(bytes(size), ())


@pytest.mark.parametrize("scale", [0, 3])
def test_rejects_unsupported_scales(scale):
    with pytest.raises(ValueError, match="Scale must be 1 or 2"):
        render_chr_sheets(bytes(8192), (), scale)
