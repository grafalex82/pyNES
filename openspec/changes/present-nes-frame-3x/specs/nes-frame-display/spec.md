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

The window title SHALL show the number of frames actually presented per elapsed wall-clock second, refreshed at
least once per host update after one second has elapsed. The initial preview counts as a presentation. The rate
SHALL be zero when no frames are presented during the measurement interval and SHALL NOT limit emulation speed.

#### Scenario: Present frames during a measurement interval

- **WHEN** the window presents three frames during a 1.5 second interval
- **THEN** the next rate update shows `2.0 FPS` in the title

#### Scenario: No new presentation

- **WHEN** one second passes without presenting any frames
- **THEN** the next rate update shows `0.0 FPS` in the title
