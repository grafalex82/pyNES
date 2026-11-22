# background-tile-inspection Specification

## Purpose

Make the stationary background's nametable tile numbers and effective colors visible for emulator study.

## Requirements

### Requirement: Toggle the inspection view

The emulator SHALL start in normal image mode. Each F1 key-down SHALL toggle between normal and background tile
inspection modes independently of the logging option. The selected mode SHALL apply to subsequent completed frames.

#### Scenario: Toggle twice

- **WHEN** the user presses and releases F1, then presses and releases it again
- **THEN** the inspection view is shown after the first press and the normal image after the second
- **AND** emulation continues in the same window

### Requirement: Show stationary nametable tile numbers

The inspection view SHALL show all 32 by 30 tile bytes from the stationary $2000 nametable, including when the
background layer is disabled. Each 8 by 8 cell SHALL show the byte as two uppercase hexadecimal digits, including a
leading zero, using white 3 by 7 pixel glyphs on black. A black column SHALL separate the glyphs and follow the second.

#### Scenario: Inspect tile bytes with the background disabled

- **WHEN** background rendering is disabled and the first and last nametable cells contain $0A and $F5
- **THEN** their cells display `0A` and `F5` respectively in the inspection view
- **AND** the view covers the full native 256 by 240 pixel frame

### Requirement: Show effective palette colors

The bottom row of each inspection cell SHALL show four adjacent two-pixel-wide color swatches in pattern-index order.
The first SHALL use the universal backdrop at $3F00; the other three SHALL use the colors of the subpalette selected
by that cell's attribute quadrant. Swatches SHALL use the same RGB conversion as normal rendering.

#### Scenario: Inspect attribute quadrants

- **WHEN** adjacent 16 by 16 attribute quadrants select different subpalettes with distinct colors
- **THEN** each tile in a quadrant displays the shared backdrop followed by that quadrant's three selected colors
- **AND** each swatch occupies two native pixels in the eighth row of its tile cell

### Requirement: Use a coherent completed frame

The inspection view SHALL use nametable and palette values sampled at the same frame boundary as the associated
normal frame. Switching modes SHALL NOT change emulated memory, registers, or CPU execution.

#### Scenario: Memory changes after capture

- **WHEN** nametable or palette memory changes after a frame has been captured but before it is presented
- **THEN** the inspection view for that captured frame displays the values at capture, not the later values
