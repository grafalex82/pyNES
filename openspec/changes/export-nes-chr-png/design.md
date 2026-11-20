# Design

## Context

See [proposal.md](proposal.md) for the motivation. `NESFile` already extracts the CHR section after any trainer
and PRG bytes. `misc\disassemble.py` shows how a standalone utility imports that loader without starting emulation
and keeps user-supplied paths relative to the caller's working directory. `requirements.txt` currently lists only
pytest; PNG output introduces pygame as a dependency for the exporter.

## Goals / Non-Goals

**Goals:** Keep file handling, tile decoding, and image composition in one standalone script. Preserve CHR byte
order and keep the preview layout independent of tile color and scale.

**Non-Goals:** Do not create a reusable rendering subsystem, route reads through `Machine`, or infer which PPU
pattern table the game uses for sprites or backgrounds.

## Decisions

1. **Reuse the cartridge loader; split the extracted bytes at 4 KiB.** Keep both sheets in file order. The suffixes
   are offsets within CHR, not claims about the mapper's runtime configuration. No mapper restriction is needed for
   a static 8 KiB export. Reject other sizes instead of silently choosing a bank or dropping tiles.
2. **Decode one tile at a time.** In each 16-byte tile, the first eight bytes contain the low bits and the second
   eight the high bits. Pair the two row bytes and read each from bit 7 to bit 0 to obtain four possible pixel
   values. This is the [NES tile layout](https://bugzmanov.github.io/nes_ebook/chapter_6_3.html); use a direct decoder
   rather than trying to derive colors or metatiles from the raw bytes.
3. **Use one grammar for both palette inputs.** Split the inline string or UTF-8 file on whitespace and check
   that each token is two hex digits in range. Share a group of four codes or map two groups in sheet order.
   The default RGB levels are `#000000`, `#555555`, `#AAAAAA`, and `#FFFFFF`. For custom codes, use the 64 RGB
   values from [fogleman/nes](https://github.com/fogleman/nes/blob/master/nes/palette.go) as a fixed approximation
   and retain the [MIT notice](https://github.com/fogleman/nes/blob/master/LICENSE.md) with the table. Use the
   values only, not the emulator's implementation. A textual code list avoids a separate binary palette format.
4. **Compose directly at the final size.** Use an off-screen pygame surface with per-pixel alpha. Reserve one
   output pixel between every adjacent tile row and column. Draw each decoded pixel as a single pixel or a
   solid block of four, so there is no resampling. Paint gutters `#808080` on alternating positions using the
   parity of the sum of the output coordinates, leaving the other positions transparent. The same parity rule
   handles intersections. Scaling a finished sheet would also scale the gutters, so scale only the tile pixels.
5. **Resolve supported inputs before writing.** Use `argparse` for the CLI and report unsupported CHR sizes,
   malformed palette arguments, and path conflicts before saving either image. Follow the disassembler's precedent
   for resolving output aliases: check resolved paths and existing file identity before writing. Existing PNGs
   can be replaced as long as neither aliases an input or the other destination. Keep the existing loader's
   unsupported-format behavior. Use `pygame.image.save` on the two surfaces without initializing a display.

## Risks / Trade-offs

- One RGB approximation and one palette per sheet cannot reproduce game colors; document the PNGs as previews.
  Index 0 is opaque in a tile even when a game would use it as sprite transparency.
- PNG output requires a pygame build with PNG support. Document installation for the new command without changing
  how the existing emulator and inspection scripts start.
