"""Verify CHR tile decoding and sheet composition with synthetic bitplanes."""

from pathlib import Path
import subprocess
import sys

import pygame
import pytest

from misc.chr2png import decode_tile, parse_options, render_chr_sheets


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


@pytest.mark.parametrize("scale,size", [(1, 143), (2, 271), (3, 399), (4, 527)])
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


@pytest.mark.parametrize("scale", [1, 2, 3, 4])
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


@pytest.mark.parametrize("scale", [0, 5])
def test_rejects_unsupported_scales(scale):
    with pytest.raises(ValueError, match="Scale must be 1 through 4"):
        render_chr_sheets(bytes(8192), (), scale)


def test_default_palette_and_scale_color_both_sheets():
    # Four consecutive pixels use all indices so that their RGB order and alpha can be inspected.
    args = parse_options(["game.nes", "tiles"])
    chr_rom = bytearray(8192)
    for offset in (0, 4096):
        chr_rom[offset] = 0x50
        chr_rom[offset + 8] = 0x30
    sheets = render_chr_sheets(chr_rom, args.palettes, args.scale)

    # The default uses the same opaque black-to-white palette on each half.
    assert args.scale == 1
    assert args.palette_file is None
    expected = ((0, 0, 0, 255), (85, 85, 85, 255), (170, 170, 170, 255), (255, 255, 255, 255))
    for surface in sheets:
        assert tuple(surface.get_at((x, 0)) for x in range(4)) == expected


def test_shared_inline_palette_and_scale():
    # Lowercase and uppercase spellings refer to the same NES colors.
    args = parse_options(["game.nes", "tiles", "--palette", "0f 01 21 30", "--scale", "2"])
    expected = ((0, 0, 0), (0, 42, 136), (100, 176, 255), (255, 254, 255))
    assert args.palettes == (expected, expected)
    assert args.scale == 2


def test_palette_file_matches_inline_two_sheet_colors(tmp_path):
    # Newlines and spaces use the same grammar regardless of the palette source.
    palette_file = tmp_path / "palette colors.txt"
    palette_file.write_text("0F 01 21 30\n0f 06 16 26\n", encoding="utf-8")
    from_file = parse_options(["game.nes", "tiles", "--palette-file", str(palette_file)])
    inline = parse_options(["game.nes", "tiles", "--palette", "0F 01 21 30 0f 06 16 26"])

    # Each sheet receives its own palette, and equivalent inputs produce the same rendered pixels.
    assert from_file.palette_file == str(palette_file)
    assert from_file.palettes == inline.palettes
    expected = (
        ((0, 0, 0), (0, 42, 136), (100, 176, 255), (255, 254, 255)),
        ((0, 0, 0), (108, 6, 0), (181, 49, 32), (254, 129, 112)),
    )
    assert from_file.palettes == expected
    chr_rom = bytearray(8192)
    for offset in (0, 4096):
        chr_rom[offset] = 0x50
        chr_rom[offset + 8] = 0x30
    file_sheets = render_chr_sheets(chr_rom, from_file.palettes)
    inline_sheets = render_chr_sheets(chr_rom, inline.palettes)
    for sheet, colors in enumerate(expected):
        assert pygame.image.tobytes(file_sheets[sheet], "RGBA") == pygame.image.tobytes(inline_sheets[sheet], "RGBA")
        for x, color in enumerate(colors):
            assert file_sheets[sheet].get_at((x, 0)) == (*color, 255)
            assert inline_sheets[sheet].get_at((x, 0)) == (*color, 255)


def test_accepts_palette_code_boundaries():
    args = parse_options(["game.nes", "tiles", "--palette", "00 3F 00 3f"])
    expected = ((102, 102, 102), (0, 0, 0), (102, 102, 102), (0, 0, 0))
    assert args.palettes == (expected, expected)


@pytest.mark.parametrize("palette", ["", "00 01 02", "00 01 02 03 04", "00 01 02 40", "00 01 02 0x03",
                                      "00 01 02 gg", "00 01 02 \uff10\uff10"])
def test_rejects_invalid_inline_palettes(palette, capsys):
    with pytest.raises(SystemExit) as error:
        parse_options(["game.nes", "tiles", "--palette", palette])
    assert error.value.code == 2
    assert "palette" in capsys.readouterr().err


def test_rejects_invalid_palette_file(tmp_path, capsys):
    palette_file = tmp_path / "palette.txt"
    palette_file.write_text("00 01 02 40", encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        parse_options(["game.nes", "tiles", "--palette-file", str(palette_file)])
    assert error.value.code == 2
    assert "palette" in capsys.readouterr().err


def test_rejects_conflicting_palette_sources(capsys):
    with pytest.raises(SystemExit) as error:
        parse_options(["game.nes", "tiles", "--palette", "00 01 02 03", "--palette-file", "colors.txt"])
    assert error.value.code == 2
    assert "not allowed with argument" in capsys.readouterr().err


@pytest.mark.parametrize("scale", ["0", "5", "1.5", "no"])
def test_rejects_invalid_scale_option(scale, capsys):
    with pytest.raises(SystemExit) as error:
        parse_options(["game.nes", "tiles", "--scale", scale])
    assert error.value.code == 2
    assert "--scale" in capsys.readouterr().err


@pytest.fixture
def make_chr_cartridge(tmp_path):
    def create_file(filename="game with spaces.nes", chr_banks=1):
        # A nonzero mapper and trainer demonstrate that static CHR extraction does not emulate mapping.
        header = b"NES\x1a" + bytes([1, chr_banks, 0x14, 0]) + bytes(8)
        chr_rom = bytearray(chr_banks * 8192)
        if chr_rom:
            chr_rom[0] = 0x80
            chr_rom[4096 + 8] = 0x80
        cartridge = tmp_path / filename
        cartridge.write_bytes(header + bytes([0xA5]) * 512 + bytes([0x5A]) * 16384 + chr_rom)
        return cartridge

    return create_file


def run_chr_command(directory, *arguments):
    script = Path(__file__).resolve().parents[1] / "misc" / "chr2png.py"
    return subprocess.run([sys.executable, str(script), *arguments], cwd=directory, capture_output=True, text=True)


@pytest.mark.parametrize("scale", [1, 2, 3, 4])
def test_exports_cartridge_pngs_from_another_directory(tmp_path, make_chr_cartridge, scale):
    # Distinct tile bitplanes and palette groups make incorrect CHR offsets or sheet order visible.
    cartridge = make_chr_cartridge()
    original = cartridge.read_bytes()
    palette = tmp_path / "palette colors.txt"
    palette.write_text("0F 01 21 30\n0F 06 16 26\n", encoding="utf-8")
    first = tmp_path / "tile sheet-0000.png"
    second = tmp_path / "tile sheet-1000.png"
    first.write_bytes(b"old first")
    second.write_bytes(b"old second")

    # Run outside the repository and inspect actual PNG bytes and decoded surface pixels.
    result = run_chr_command(
        tmp_path, cartridge.name, "tile sheet", "--palette-file", palette.name, "--scale", str(scale)
    )
    assert result.returncode == 0, result.stderr
    assert cartridge.read_bytes() == original
    assert palette.read_text(encoding="utf-8") == "0F 01 21 30\n0F 06 16 26\n"
    for path, color in ((first, (0, 42, 136, 255)), (second, (181, 49, 32, 255))):
        assert path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        image = pygame.image.load(path)
        assert image.get_size() == (128 * scale + 15, 128 * scale + 15)
        for y in range(scale):
            for x in range(scale):
                assert image.get_at((x, y)) == color
        assert image.get_at((8 * scale, 0)) == (128, 128, 128, 255)
        assert image.get_at((8 * scale, 1)).a == 0


@pytest.mark.parametrize("chr_banks,message", [(0, "no CHR ROM"), (2, "CHR ROM size 16384 bytes")])
def test_rejects_unsupported_chr_before_writing(tmp_path, make_chr_cartridge, chr_banks, message):
    # Existing output is preserved and the missing output remains absent.
    cartridge = make_chr_cartridge(chr_banks=chr_banks)
    original = cartridge.read_bytes()
    first = tmp_path / "tiles-0000.png"
    second = tmp_path / "tiles-1000.png"
    first.write_bytes(b"existing output")

    result = run_chr_command(tmp_path, cartridge.name, "tiles")
    assert result.returncode != 0
    assert message in result.stderr
    assert first.read_bytes() == b"existing output"
    assert not second.exists()
    assert cartridge.read_bytes() == original


@pytest.mark.parametrize("suffix", ["0000", "1000"])
@pytest.mark.parametrize("input_kind", ["cartridge", "palette"])
def test_rejects_output_hard_links_to_inputs(tmp_path, make_chr_cartridge, suffix, input_kind):
    # Both ROM and palette are inputs even when their content is reached through an output hard link.
    cartridge = make_chr_cartridge()
    palette = tmp_path / "colors.txt"
    palette.write_text("0F 01 21 30", encoding="utf-8")
    source = cartridge if input_kind == "cartridge" else palette
    original = source.read_bytes()
    alias = tmp_path / f"tiles-{suffix}.png"
    alias.hardlink_to(source)
    other_suffix = "1000" if suffix == "0000" else "0000"
    other = tmp_path / f"tiles-{other_suffix}.png"
    other.write_bytes(b"existing output")

    result = run_chr_command(tmp_path, cartridge.name, "tiles", "--palette-file", palette.name)
    assert result.returncode != 0
    assert "must not identify input" in result.stderr
    assert source.read_bytes() == original
    assert alias.read_bytes() == original
    assert other.read_bytes() == b"existing output"


def test_rejects_output_paths_that_are_hard_links(tmp_path, make_chr_cartridge):
    cartridge = make_chr_cartridge()
    first = tmp_path / "tiles-0000.png"
    second = tmp_path / "tiles-1000.png"
    first.write_bytes(b"shared output")
    second.hardlink_to(first)

    result = run_chr_command(tmp_path, cartridge.name, "tiles")
    assert result.returncode != 0
    assert "distinct files" in result.stderr
    assert first.read_bytes() == b"shared output"
    assert second.read_bytes() == b"shared output"


@pytest.mark.parametrize("suffix", ["0000", "1000"])
@pytest.mark.parametrize("input_kind", ["cartridge", "palette"])
def test_rejects_output_path_identical_to_input(tmp_path, make_chr_cartridge, suffix, input_kind):
    # Either generated filename can also be the literal name of a valid input.
    filename = f"tiles-{suffix}.png"
    cartridge = make_chr_cartridge(filename if input_kind == "cartridge" else "game.nes")
    palette = tmp_path / (filename if input_kind == "palette" else "colors.txt")
    palette.write_text("0F 01 21 30", encoding="utf-8")
    original_cartridge = cartridge.read_bytes()
    original_palette = palette.read_bytes()
    other_suffix = "1000" if suffix == "0000" else "0000"
    other = tmp_path / f"tiles-{other_suffix}.png"
    other.write_bytes(b"existing output")

    result = run_chr_command(tmp_path, cartridge.name, "tiles", "--palette-file", palette.name)
    assert result.returncode != 0
    assert "must not identify input" in result.stderr
    assert cartridge.read_bytes() == original_cartridge
    assert palette.read_bytes() == original_palette
    assert other.read_bytes() == b"existing output"


def test_invalid_palette_does_not_replace_outputs(tmp_path, make_chr_cartridge):
    cartridge = make_chr_cartridge()
    first = tmp_path / "tiles-0000.png"
    second = tmp_path / "tiles-1000.png"
    first.write_bytes(b"existing output")

    result = run_chr_command(tmp_path, cartridge.name, "tiles", "--palette", "00 01 02 40")
    assert result.returncode != 0
    assert "palette" in result.stderr
    assert first.read_bytes() == b"existing output"
    assert not second.exists()


@pytest.mark.parametrize("scale", ["0", "5"])
def test_invalid_scale_does_not_replace_outputs(tmp_path, make_chr_cartridge, scale):
    # Preserve an existing output while leaving the second output absent.
    cartridge = make_chr_cartridge()
    first = tmp_path / "tiles-0000.png"
    second = tmp_path / "tiles-1000.png"
    first.write_bytes(b"existing output")

    # Invalid scales must be rejected before either output is written.
    result = run_chr_command(tmp_path, cartridge.name, "tiles", "--scale", scale)
    assert result.returncode != 0
    assert "--scale" in result.stderr
    assert first.read_bytes() == b"existing output"
    assert not second.exists()


def test_exports_with_default_palette(tmp_path, make_chr_cartridge):
    cartridge = make_chr_cartridge()
    result = run_chr_command(tmp_path, cartridge.name, "tiles")
    assert result.returncode == 0, result.stderr
    first = pygame.image.load(tmp_path / "tiles-0000.png")
    second = pygame.image.load(tmp_path / "tiles-1000.png")
    assert first.get_at((0, 0)) == (85, 85, 85, 255)
    assert second.get_at((0, 0)) == (170, 170, 170, 255)
