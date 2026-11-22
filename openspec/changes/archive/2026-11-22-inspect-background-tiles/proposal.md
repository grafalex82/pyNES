# Proposal

## Why

The rendered background hides the nametable bytes and palette selections that produced it. A compact inspection
view will make those relationships visible while learning how NES background rendering works.

## What Changes

- Toggle a background tile inspection view with F1; normal rendering remains the startup default.
- Show each stationary background tile's hexadecimal number and its four effective background colors.
- Permit inspection even when background rendering is disabled, using the same frame-boundary state as the image.
- Limit this change to the currently implemented stationary $2000 nametable; sprites and scrolling remain future work.

## Capabilities

### New Capabilities

- `background-tile-inspection`: Inspect background tile numbers and effective palette colors in the emulator window.

### Modified Capabilities

None.

## Impact

The PPU's frame capture, the host event loop and display, focused synthetic tests, and user documentation are affected.
The existing frame display and PPU rendering specifications are in the unfinished `present-nes-frame-3x` change; this
proposal builds on their currently implemented stationary background subset without claiming its remaining features.
