# Video Register Routing

## MODIFIED Requirements

### Requirement: Report unimplemented CPU address ranges

Reads at $2000-$3FFF except aliases of $2002, $2004, and $2007 SHALL raise NotImplementedError. Reads at
$4000-$7FFF except $4010-$4013 and $4015 and writes there except $4010-$4015 and $4017 SHALL raise that error.
PPU-window access SHALL route to the PPU. Reads and writes at $4010-$4013 and $4015 SHALL route to the audio
component. Writes at $4017 SHALL route to the audio component and have no frame-counter or IRQ effects.
PPU read errors SHALL identify the operation and register offset. Other errors SHALL identify the operation
and CPU address. Unimplemented ranges SHALL NOT act as RAM.

#### Scenario: Access an unimplemented address

- **WHEN** an access targets an unsupported PPU read port or an unimplemented address in $4000-$7FFF
- **THEN** NotImplementedError identifies the attempted operation and PPU register offset or CPU address, respectively

#### Scenario: Access sprite DMA

- **WHEN** a read targets $4014
- **THEN** NotImplementedError identifies the read and address $4014

#### Scenario: Write a PPU register mirror

- **WHEN** a write targets $2000-$3FFF
- **THEN** the write reaches the PPU register selected by the low three address bits

#### Scenario: Read a PPU status mirror

- **WHEN** a read targets a PPU address whose low three bits are 2
- **THEN** it returns the current status from the connected PPU and applies the status read effects

#### Scenario: Read mirrored PPU data ports

- **WHEN** a read targets a PPU address whose low three bits are 4 or 7
- **THEN** it reaches the corresponding OAMDATA or PPUDATA port with that port's read effects

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

## ADDED Requirements

### Requirement: Transfer a CPU page to sprite memory

A write of page $XX to $4014 SHALL read 256 bytes from $XX00-$XXFF through Machine in ascending order and
store them in OAM starting at the current OAM address, wrapping at $FF. The functional transfer completes
synchronously without a CPU stall.

#### Scenario: Transfer from a CPU RAM mirror

- **WHEN** software writes $0A to $4014 with OAMADDR set to $F0 and a distinguishable page at $0200-$02FF
- **THEN** the first byte goes to OAM $F0, the seventeenth to $00, and the last to $EF
- **AND** OAMADDR is $F0 after all 256 writes
