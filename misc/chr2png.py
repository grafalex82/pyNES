"""Export cartridge CHR tiles to two offline PNG sheets."""

import argparse
from pathlib import Path
import re
import sys

import pygame

# Resolve component imports from this file so callers can use any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nesfile import NESFile
from nes_palette import NES_COLORS


DEFAULT_PALETTE = ((0, 0, 0), (85, 85, 85), (170, 170, 170), (255, 255, 255))


def parse_palettes(text):
    """Convert four or eight whitespace-separated NES hex codes into two four-color RGB palettes."""
    # Each NES code selects one RGB approximation; reject other hexadecimal spellings and out-of-range values.
    codes = text.split()
    if len(codes) not in (4, 8):
        raise ValueError("palette must contain exactly 4 or 8 NES color codes")
    if any(not re.fullmatch(r"[0-9a-fA-F]{2}", code) or int(code, 16) > 0x3F for code in codes):
        raise ValueError("palette codes must be two hexadecimal digits from 00 to 3F")

    # Four entries are shared; eight select independent palettes in sheet order.
    colors = tuple(tuple(NES_COLORS[int(code, 16)].to_bytes(3, "big")) for code in codes)
    first = colors[:4]
    return first, colors[4:] if len(colors) == 8 else first


def parse_options(argv=None):
    """Parse export options and return paths, scale, and two RGB palettes."""
    # Both palette sources use the same textual format and cannot be selected simultaneously.
    parser = argparse.ArgumentParser(description="Export CHR ROM tiles to two PNG sheets.")
    parser.add_argument("rom", help="path to a valid iNES or NES 2.0 cartridge file")
    parser.add_argument("output", help="output filename prefix")
    palette_group = parser.add_mutually_exclusive_group()
    palette_group.add_argument("--palette", help="4 or 8 whitespace-separated NES hex color codes")
    palette_group.add_argument("--palette-file", help="UTF-8 file containing 4 or 8 NES hex color codes")
    parser.add_argument("--scale", type=int, choices=(1, 2, 3, 4), default=1, help="tile pixel scale (default: 1)")
    args = parser.parse_args(argv)

    # Read a selected file before parsing; filesystem errors remain visible to the caller.
    palette_text = args.palette
    if args.palette_file is not None:
        palette_text = Path(args.palette_file).read_text(encoding="utf-8")
    if palette_text is None:
        args.palettes = (DEFAULT_PALETTE, DEFAULT_PALETTE)
    else:
        try:
            args.palettes = parse_palettes(palette_text)
        except ValueError as error:
            parser.error(str(error))
    return args


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
    pixel index. Scale is 1 through 4 and affects tile pixels only. The returned surfaces are in CHR file order.
    """
    # A complete sheet pair avoids silently discarding data or inventing tiles.
    if len(chr_rom) != 8192:
        raise ValueError(f"Expected 8192 bytes of CHR ROM, got {len(chr_rom)}")
    if scale not in (1, 2, 3, 4):
        raise ValueError(f"Scale must be 1 through 4, got {scale}")

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


def same_file(first, second):
    """Identify matching paths or existing hard links without requiring outputs to exist."""
    return first.resolve() == second.resolve() or (first.exists() and second.exists() and first.samefile(second))


def main():
    # Both output paths are relative to the caller's working directory, like the input paths.
    args = parse_options()
    outputs = [Path(f"{args.output}-0000.png"), Path(f"{args.output}-1000.png")]
    inputs = [Path(args.rom)]
    if args.palette_file is not None:
        inputs.append(Path(args.palette_file))

    # Refuse path aliases and hard links before either output is opened.
    if same_file(outputs[0], outputs[1]):
        raise SystemExit("output paths must identify distinct files")
    for output in outputs:
        for source in inputs:
            if same_file(output, source):
                raise SystemExit(f"output path {output} must not identify input {source}")

    # CHR RAM and banked CHR are not equivalent to an 8 KiB static ROM export.
    chr_rom = NESFile(args.rom).get_chr_rom()
    if not chr_rom:
        raise NotImplementedError("Cartridge has no CHR ROM; CHR RAM export is not implemented")
    if len(chr_rom) != 8192:
        raise NotImplementedError(f"CHR ROM size {len(chr_rom)} bytes is not supported; expected 8192 bytes")
    sheets = render_chr_sheets(chr_rom, args.palettes, args.scale)

    # Surfaces are complete before saving, so unsupported inputs cannot truncate existing outputs.
    for surface, output in zip(sheets, outputs):
        pygame.image.save(surface, output)


if __name__ == "__main__":
    main()
