# CPU Memory Delta

## MODIFIED Requirements

### Requirement: Report unimplemented CPU address ranges

Reads at $2000-$3FFF except aliases of $2002 and $2007 and reads at $4000-$7FFF except $4010-$4013 and $4015-$4017 SHALL
raise NotImplementedError. Writes at $4000-$7FFF except $4000, $4004 and $4010-$4017 SHALL raise NotImplementedError.
PPU-window access SHALL route to the PPU. Reads and writes at $4010-$4013 and $4015 SHALL route to the audio component.
Writes at $4000 and $4004 SHALL route to the audio component without pulse-channel effects; writes
at $4017 SHALL route to the audio component without frame-counter or IRQ effects. Writes at $4014 and $4016 SHALL be
accepted without effects. Controller reads at $4016 and $4017 SHALL return $00. PPU read errors SHALL identify the
operation and register offset; other errors SHALL identify the operation and CPU address. Unimplemented ranges SHALL
NOT act as RAM.

#### Scenario: Access an unimplemented address

- **WHEN** a read or write targets an otherwise unimplemented address
- **THEN** NotImplementedError identifies the operation and PPU register offset or CPU address

#### Scenario: Access sprite DMA

- **WHEN** a read targets $4014 or a byte is written to $4014
- **THEN** the read raises NotImplementedError and the write is ignored without transfer or DMA stall

#### Scenario: Write a PPU register mirror

- **WHEN** a write targets $2000-$3FFF
- **THEN** the write reaches the PPU register selected by the low three address bits

#### Scenario: Read a PPU status mirror

- **WHEN** a read targets a PPU address whose low three bits are 2
- **THEN** it returns the status byte from the connected PPU

#### Scenario: Access a selected audio register

- **WHEN** a read or write targets $4010, $4011, $4012, $4013, or $4015
- **THEN** the operation reaches the connected audio component

#### Scenario: Write the frame-counter register

- **WHEN** any byte is written to $4017
- **THEN** the audio component accepts the write without frame-counter or IRQ effects
- **AND** subsequent dummy audio status reads still return $00

#### Scenario: Read the second controller address

- **WHEN** a read targets $4017
- **THEN** the result is $00 without reading the APU

#### Scenario: Write the first controller address

- **WHEN** any byte is written to $4016
- **THEN** the write completes without controller strobe or button effects
- **AND** reads at $4016 return $00

#### Scenario: Write pulse channel control

- **WHEN** a byte is written to $4000
- **THEN** it reaches the audio component and has no pulse-channel effects
- **AND** CPU reads at $4000 remain unsupported

#### Scenario: Write pulse 2 channel control

- **WHEN** a byte is written to $4004
- **THEN** it reaches the audio component and has no pulse-channel effects
- **AND** CPU reads at $4004 remain unsupported

#### Scenario: Repeated controller reads

- **WHEN** either controller address is read repeatedly, with or without strobe writes
- **THEN** each read returns $00
