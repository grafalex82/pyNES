# Standard controller input

## Purpose

Expose standard NES controller button states to software and provide fixed keyboard controls for two players.

## ADDED Requirements

### Requirement: Latch and read standard controllers

Two connected standard controllers SHALL share bit 0 of writes to $4016 as their strobe. Each port SHALL return its own
button state in bit 0, with bits 1-7 zero. A pressed button SHALL read as 1 and a released button as 0.

#### Scenario: Strobe and read both controllers

- **WHEN** software writes bit 0 as 1 and then 0 at $4016 and reads each controller port eight times
- **THEN** each port returns its latched buttons in order A, B, Select, Start, Up, Down, Left, Right
- **AND** reading one port does not advance the other port

#### Scenario: Change buttons after latching

- **WHEN** button states change after the strobe goes low and before all eight reads complete
- **THEN** the current serial reports retain the states latched when the strobe went low
- **AND** a subsequent high-to-low strobe captures the changed states

#### Scenario: Read while strobe is high

- **WHEN** the strobe is high and a controller port is read repeatedly while its A button changes
- **THEN** each read reports the current A button state without advancing the serial report

#### Scenario: Read after all buttons

- **WHEN** a connected controller is read more than eight times while strobe remains low
- **THEN** every subsequent read returns $01 until a new strobe

#### Scenario: Write unrelated strobe bits or repeat low

- **WHEN** software changes only bits 1-7 of $4016 or writes bit 0 as 0 again while it is already low
- **THEN** neither operation relatches or restarts either controller report

### Requirement: Map keyboard controls to both controllers

The emulator SHALL map fixed host keys to both controllers, preserving simultaneous button states. Player 1 uses
arrows for directions, period for A, comma for B, Enter for Start, and right Shift for Select. Player 2 uses
W/S/A/D for Up/Down/Left/Right, G for A, F for B, T for Start, and R for Select.

#### Scenario: Press and release keys

- **WHEN** the window has focus and mapped keys are pressed and released
- **THEN** the associated button states follow those keys independently without requiring Shift for comma or period
- **AND** a later strobe captures all buttons still held

#### Scenario: Lose keyboard focus

- **WHEN** the window loses keyboard focus while mapped keys are held
- **THEN** both controllers' current buttons are released
- **AND** a report already latched remains unchanged until the next strobe

#### Scenario: Toggle background inspection

- **WHEN** F1 is pressed
- **THEN** it retains its background-inspection behavior and does not change either controller's buttons
