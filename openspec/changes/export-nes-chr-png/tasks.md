# Tasks

## 1. CHR sheet composition

- [x] 1.1 Add the two-bitplane decoder to `misc\chr2png.py` and verify all four pixel values and bit order using
  an asymmetric synthetic tile.
- [x] 1.2 Add pygame to `requirements.txt` and render both sheets without a display; verify tile order, image sizes,
  exact pixel doubling, and horizontal and vertical one-pixel gutters at both scales.

## 2. Command-line export

- [x] 2.1 Parse the shared palette grammar and scale options; verify the default grayscale, shared inline and
  per-sheet file palettes, matching inline/file results, and errors for malformed or conflicting arguments.
- [x] 2.2 Wire `NESFile` and PNG saving to the command. Verify with synthetic cartridges that a call from another
  directory produces the named PNGs with the expected pixels and leaves inputs untouched. Check that empty or
  oversized CHR and output path conflicts fail without creating or replacing either PNG.
- [x] 2.3 Add command examples and installation notes to `README.md` and record the preview color approximation
  in `doc\decisions.md`. Run a documented invocation against a synthetic cartridge to verify the example.
- [x] 2.4 Support integer scales 1 through 4 in the renderer and CLI. Verify scales 3 and 4, including tile pixels,
  both sheet sizes, and one-pixel gutters; reject out-of-range values. Update the usage and decision record.
