# Design

## Context

The PPU renders a stationary $2000 background and publishes RGB frames at vblank. The host presents the newest
published frame after each bounded CPU block. It currently retains no tile metadata with the frame. See the proposal
and inspection specification for scope and observable behavior.

## Goals / Non-Goals

**Goals:** Keep inspection synchronized with the existing whole-frame approximation and independent of emulated state.

**Non-Goals:** Implement scrolling, sprite inspection, actual PPU timing, new palette behavior, or ROM modifications.

## Decisions

### Capture matching inspection data at vblank

Capture the tile bytes, attribute data and effective palette colors at the same boundary as the RGB frame, then build
the inspection image from that immutable data. This avoids sampling live VRAM after the CPU has continued. A separate
live VRAM read at presentation was considered but could describe a different frame. Preserve the initial preview and
the latest matching capture when switching modes; display the selected view at the next completed frame.

### Reflect the current background model

Read 960 tile bytes from $2000 and derive each two-bit palette selection from the same attribute quadrant calculation
as normal rendering. NES attributes select one of four background subpalettes for each 2 by 2 tile region; pattern
index zero uses the shared backdrop, while indices 1 through 3 use the selected subpalette. Use the existing RGB table.
The stationary nametable, whole-frame sampling and fixed RGB conversion are existing approximations, not new hardware
behavior. The diagnostic view is a host visualization and does not change what software reads or writes.

### Draw an explicit bitmap font and swatches

Use a small fixed 3 by 7 hexadecimal bitmap font in native frame pixels: two digits, one black separator and a black
rightmost column. Four pairs of pixels in the final row show effective colors. Fixed white glyphs on black guarantee
legibility regardless of game palette; a system font would vary across machines. Reuse the existing 3x presenter.
Swatches show actual colors rather than numeric palette IDs; identical subpalettes can therefore be indistinguishable.

### Keep mode selection in the host

Handle F1 key-down in the existing event loop and select which captured image to present. It is independent of the
`--debug` logging flag. Keep the existing FPS title; showing the pattern table in the title is deferred because the
tile number and color inspection do not require a title change. Do not route the host key into emulated controllers.

## Risks / Trade-offs

- [Capture and drawing add work per frame] -> Keep the representation small and use focused tests; avoid a framework.
- [Future scrolling and sprites make fixed cells misleading] -> Document this view's stationary-background scope and
  revisit it with those features rather than implying that it represents sprite composition or scrolled pixels.
- [Normal and inspection frames can diverge] -> Test a write between capture and presentation and verify both are
  associated with the same frame boundary.
