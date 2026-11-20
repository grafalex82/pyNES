# Proposal

## Why

The cartridge loader exposes CHR ROM bytes, but inspecting the target games' artwork currently requires an external
viewer. An offline export makes it possible to study how NES bitplanes encode tiles before implementing PPU rendering.

## What Changes

- Add a standalone command that exports exactly 8 KiB of CHR ROM as two PNG sheets of 256 tiles each.
- Default to four opaque grayscale levels. Accept one shared NES preview palette or one per sheet, from either
  hexadecimal command-line values or a text file.
- Separate tiles with one-pixel gray dotted gutters. Optionally double each tile pixel without widening the gutters.
- Leave game palette discovery, CHR RAM, and larger banked CHR exports out of scope.

## Capabilities

### New Capabilities

- `nes-chr-export`: Offline conversion of an 8 KiB cartridge CHR ROM section to two tile sheets.

### Modified Capabilities

## Impact

- Add `misc/chr2png.py` as a consumer of `NESFile.get_chr_rom()`, with no changes to the cartridge parser or emulator.
- Use pygame for PNG output without a window. Add installation and usage notes and focused synthetic pytest coverage.
