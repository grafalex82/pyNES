# Spec Delta

## MODIFIED Requirements

### Requirement: Report unimplemented CPU address ranges

Reads at $2000-$3FFF except status-register aliases and reads at $4000-$7FFF except $4010-$4013 and $4015 SHALL
raise NotImplementedError. Writes at $4000-$7FFF except $4010-$4013, $4015, and $4017 SHALL raise NotImplementedError.
PPU-window writes and status reads SHALL route to the PPU. Reads and writes at $4010-$4013 and $4015 SHALL route
to the audio component. Writes at $4017 SHALL route to the audio component and have no frame-counter or IRQ effects.
PPU read errors SHALL identify the operation and register offset; other errors SHALL identify the operation and CPU
address. Unimplemented ranges SHALL NOT act as RAM.

#### Scenario: Access an unimplemented address

- **WHEN** a read targets a non-status PPU register or an unimplemented address in $4000-$7FFF, or a write targets
  an unimplemented address in $4000-$7FFF
- **THEN** NotImplementedError identifies the attempted operation and PPU register offset or CPU address, respectively

#### Scenario: Access sprite DMA

- **WHEN** a read or write targets $4014
- **THEN** NotImplementedError identifies the attempted operation and CPU address

#### Scenario: Write a PPU register mirror

- **WHEN** a write targets $2000-$3FFF
- **THEN** the write reaches the PPU register selected by the low three address bits

#### Scenario: Read a PPU status mirror

- **WHEN** a read targets a PPU address whose low three bits are 2
- **THEN** it returns the next status byte from the connected PPU

#### Scenario: Access a selected audio register

- **WHEN** a read or write targets $4010, $4011, $4012, $4013, or $4015
- **THEN** the operation reaches the connected audio component

#### Scenario: Write the frame-counter register

- **WHEN** any byte is written to $4017
- **THEN** the audio component accepts the write without frame-counter or IRQ effects
- **AND** subsequent dummy audio status reads still return $00

#### Scenario: Read the second controller address

- **WHEN** a read targets $4017
- **THEN** NotImplementedError identifies the CPU read and address $4017
