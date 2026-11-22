# NES Frame Display

## Purpose

Present complete NES-sized frames in a host window with a fixed integer scale that preserves individual pixel colors.

## ADDED Requirements

### Requirement: Present a complete NES frame at scale three

The display SHALL accept a 256 × 240 frame of packed RGB bytes in top-to-bottom row order, with pixels in each row
ordered left to right. Its window drawing area SHALL be 768 × 720 pixels. The source pixel at (x, y) SHALL fill the
3 × 3 block starting at (3x, 3y) with that pixel's exact RGB value.

#### Scenario: Present an asymmetric synthetic frame

- **WHEN** a frame with distinct colors in adjacent pixels and at the bottom-right corner is presented
- **THEN** the drawing area is 768 × 720 pixels
- **AND** each selected color fills its corresponding 3 × 3 block, including the last block at (765, 717)

### Requirement: Replace the displayed frame in the same window

Presenting a subsequent frame SHALL update the existing window with the complete new frame.

#### Scenario: Present two successive frames

- **WHEN** a second frame changes one or more source pixel colors
- **THEN** the same window displays the new colors in their corresponding blocks

### Requirement: Show the presentation rate

The window title SHALL show completed intervals between actual presentations per elapsed wall-clock second. The
initial preview starts the measurement. The rate SHALL be refreshed after at least one second and one subsequent
presentation, and retain its previous value while waiting. The measurement SHALL NOT limit emulation speed.

#### Scenario: Present frames during a measurement interval

- **WHEN** the window presents three frames spanning a 1.5 second interval
- **THEN** the next rate update shows `1.3 FPS` in the title

#### Scenario: A slow presentation

- **WHEN** a new frame is presented five seconds after the previous measurement began
- **THEN** the next rate update shows `0.2 FPS` in the title
- **AND** time spent waiting without another frame does not reset the measurement
