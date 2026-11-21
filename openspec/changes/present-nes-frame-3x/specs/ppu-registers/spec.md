# PPU Register Effects

## MODIFIED Requirements

### Requirement: Accept PPU register writes

CPU addresses $2000-$3FFF SHALL select register offset (address - $2000) modulo 8. Supported writes SHALL apply
the addressed register's effects. The PPU SHALL NOT retain every last-written byte for inspection. Writes to the
status offset SHALL be accepted without changing the vblank flag or shared address and scroll write toggle.

#### Scenario: Write through register mirrors

- **WHEN** the high and low bytes of a PPUADDR value are written through different register mirrors
- **THEN** the same address write pair selects the requested PPU address

#### Scenario: Write the status offset

- **WHEN** a byte is written to $2002 or its mirrors
- **THEN** the write is accepted without retaining it for inspection
- **AND** the vblank flag and shared address and scroll write toggle do not change

## REMOVED Requirements

### Requirement: Return alternating status values

**Reason:** Polling must observe emulated frame progress, including games that wait for an NMI instead of polling.

**Migration:** Use the vblank flag from the PPU clock and the read side effects in the status requirement.

## ADDED Requirements

### Requirement: Report vblank and reset the shared write toggle

PPUSTATUS ($2002) SHALL return the previous vblank flag in bit 7, clear it, and reset the shared address and
scroll write toggle. The other status bits SHALL read as zero in this model.

#### Scenario: Read through mirrored status ports

- **WHEN** vblank has started and software has issued the first address write
- **THEN** the first status read returns $80 and a second read before the next vblank returns $00
- **AND** the next $2005 or $2006 write starts a new pair

### Requirement: Select a PPU address and write video data

A pair of writes to PPUADDR ($2006) SHALL select the high six address bits and the low byte, in that order.
PPUDATA ($2007) writes SHALL target the selected PPU address and advance it by 1 or 32 according to $2000 bit 2
outside active rendering. PPU memory accesses SHALL use the low 14 address bits.

#### Scenario: Store data with both increment modes

- **WHEN** software writes multiple data bytes after setting a nametable address and selecting either increment
- **THEN** the written bytes land at consecutive addresses for step 1 or one tile row apart for step 32

### Requirement: Read video data through the PPUDATA buffer

A non-palette PPUDATA read outside active rendering SHALL return the previous buffered byte and refill it from
the selected address. A palette read SHALL return its six-bit color directly and refill the buffer from the
corresponding mirrored nametable address ($2F00-$2FFF). Both SHALL advance the address by the selected increment.

#### Scenario: Read cartridge data after a priming read

- **WHEN** software selects a CHR address and reads $2007 twice with increment 1
- **THEN** the second read returns the CHR byte at the selected address
- **AND** each read advances the address

#### Scenario: Read palette data directly

- **WHEN** software reads a palette address and then selects and reads a non-palette address
- **THEN** the first result is the palette color and the second is the nametable byte buffered by the palette read

### Requirement: Select the frame position through PPUCTRL and PPUSCROLL

PPUCTRL ($2000) bits 0 and 1 SHALL select the base nametable. A pair of PPUSCROLL ($2005) writes SHALL set
horizontal and vertical scroll in order using the same write toggle as PPUADDR.

#### Scenario: Use the shared write toggle

- **WHEN** software reads PPUSTATUS between a partial write pair and a new scroll pair
- **THEN** the new pair supplies the horizontal and vertical offsets for the next rendered frame

#### Scenario: Switch ports within one write pair

- **WHEN** software makes the first PPUSCROLL write and then writes PPUADDR without reading status
- **THEN** the PPUADDR write is treated as the second write and commits the current address

### Requirement: Read and write object attribute memory

OAMADDR ($2003) SHALL set the address in 256-byte OAM. An OAMDATA ($2004) write SHALL store one byte and
increment the address modulo 256. An OAMDATA read SHALL return the selected byte while preserving the address.

#### Scenario: Wrap the OAM write address

- **WHEN** software selects $FF and performs two OAMDATA writes
- **THEN** the bytes are stored at $FF and $00 and the address becomes $01
- **AND** repeated reads of a selected OAM location return its contents without advancing

### Requirement: Request NMI on a rising PPU interrupt condition

The PPU SHALL request one NMI when the combination of its vblank flag and $2000 bit 7 changes from false to true.
A high condition SHALL produce no further request until it becomes false and rises again.

#### Scenario: Enable NMI during vblank

- **WHEN** vblank starts with NMI disabled and software then enables NMI while the flag is still set
- **THEN** one request becomes pending
- **AND** repeating the enabled write produces no second request

#### Scenario: Enter vblank with NMI enabled

- **WHEN** successive frames enter vblank with the enable bit already set
- **THEN** each entry produces one request whether or not software reads PPUSTATUS
