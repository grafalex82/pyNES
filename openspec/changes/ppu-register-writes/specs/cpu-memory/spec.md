## MODIFIED Requirements

### Requirement: Report unimplemented CPU address ranges

Reads at $2000-$3FFF except status-register aliases and reads at $4000-$7FFF SHALL raise NotImplementedError.
Writes at $4000-$7FFF SHALL raise NotImplementedError. PPU-window writes and status reads SHALL route to the PPU.
Errors SHALL identify the operation and CPU address; unimplemented ranges SHALL NOT act as RAM.

#### Scenario: Access an unimplemented address

- **WHEN** a read targets a non-status PPU register or $4000-$7FFF, or a write targets $4000-$7FFF
- **THEN** NotImplementedError identifies the attempted operation and CPU address

#### Scenario: Write a PPU register mirror

- **WHEN** a write targets $2000-$3FFF
- **THEN** the write reaches the PPU register selected by the low three address bits

#### Scenario: Read a PPU status mirror

- **WHEN** a read targets a PPU address whose low three bits are 2
- **THEN** it returns the next status byte from the connected PPU
