# CPU Memory Delta

## MODIFIED Requirements

### Requirement: Report unimplemented CPU address ranges

Reads and writes in $4000-$7FFF SHALL raise NotImplementedError except for the connected APU, sprite DMA and controller
addresses described below. PPU-window access SHALL route to the PPU. Reads and writes at $4000-$4013 and $4015 SHALL
route to the audio component. Writes at $4017 SHALL route to the audio component. Writes at $4014 SHALL perform the
existing OAM transfer; reads at $4014 remain unsupported. Writes at $4016 SHALL be ignored, and reads at $4016 and
$4017 SHALL return $00. Unimplemented accesses SHALL identify the operation and PPU offset or CPU address and SHALL
NOT act as RAM.

#### Scenario: Access an unimplemented address

- **WHEN** a read or write targets an otherwise unimplemented address
- **THEN** NotImplementedError identifies the operation and PPU register offset or CPU address

#### Scenario: Access sprite DMA

- **WHEN** a read targets $4014
- **THEN** it raises NotImplementedError identifying the CPU address

#### Scenario: Write a PPU register mirror

- **WHEN** a write targets $2000-$3FFF
- **THEN** the write reaches the PPU register selected by the low three address bits

#### Scenario: Read a PPU status mirror

- **WHEN** a read targets a PPU address whose low three bits are 2
- **THEN** it returns the status byte from the connected PPU

#### Scenario: Access a selected audio register

- **WHEN** a read or write targets $4000-$4013 or $4015
- **THEN** the operation reaches the connected audio component

#### Scenario: Write the frame-counter register

- **WHEN** any byte is written to $4017
- **THEN** the audio component accepts the write without frame-counter or IRQ effects
- **AND** subsequent dummy audio status reads still return $00

#### Scenario: Read the second controller address

- **WHEN** a read targets $4017
- **THEN** the result is $00 without reading the APU

#### Scenario: Write sprite DMA

- **WHEN** a byte is written to $4014
- **THEN** the selected CPU page is copied to OAM without adding a DMA stall

#### Scenario: Write the first controller address

- **WHEN** any byte is written to $4016
- **THEN** the write completes without controller strobe or button effects
- **AND** reads at $4016 return $00

#### Scenario: Repeated controller reads

- **WHEN** either controller address is read repeatedly, with or without strobe writes
- **THEN** each read returns $00

#### Scenario: Write pulse channel control

- **WHEN** a byte is written to $4000
- **THEN** it reaches the audio component and has no pulse-channel effects
- **AND** CPU reads at $4000 return $00

#### Scenario: Write pulse 2 channel control

- **WHEN** a byte is written to $4004
- **THEN** it reaches the audio component and has no pulse-channel effects
- **AND** CPU reads at $4004 return $00

#### Scenario: Write triangle channel control

- **WHEN** a byte is written to $4008
- **THEN** it reaches the audio component and has no triangle-channel effects
- **AND** CPU reads at $4008 return $00

#### Scenario: Write noise channel control

- **WHEN** a byte is written to $400C
- **THEN** it reaches the audio component and has no noise-channel effects
- **AND** CPU reads at $400C return $00
