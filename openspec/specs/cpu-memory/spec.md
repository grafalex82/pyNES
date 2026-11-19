# cpu-memory Specification

## Purpose

Provide CPU-visible byte access to internal RAM and fixed mapper-0 cartridge ROM before processor execution is added.
Addresses are assumed valid. RAM byte-range checking is explicit; other input validation and recovery are out of scope.

## Requirements

### Requirement: Read and write internal RAM

The CPU-facing memory interface SHALL provide writable RAM at $0000-$07FF. A byte written to an address SHALL be
returned by subsequent reads of that address without changing other RAM bytes or cartridge ROM.
RAM.write_byte SHALL raise ValueError for integer values outside 0..255 without changing RAM contents.

#### Scenario: Access RAM boundaries

- **WHEN** distinct bytes are written to $0000 and $07FF
- **THEN** reads return the corresponding bytes at both boundaries and neighboring bytes remain unchanged

#### Scenario: Reject a RAM value outside one byte

- **WHEN** RAM.write_byte receives an integer below 0 or above 255 at a valid offset
- **THEN** ValueError identifies the value and the accepted range
- **AND** the target byte and all other RAM bytes remain unchanged

### Requirement: Mirror internal RAM throughout its CPU window

Addresses $0800-$1FFF SHALL refer to the same 2048 RAM bytes as $0000-$07FF, repeating every $0800 bytes.
Writes through any mirror SHALL be visible through every alias of the same physical byte.

#### Scenario: Write through each RAM mirror

- **WHEN** a byte is written through any alias of the first or last internal RAM byte
- **THEN** all corresponding aliases in $0000-$1FFF return that byte
- **AND** aliases of other RAM bytes are unchanged

### Requirement: Initialize independent RAM deterministically

A new memory configuration SHALL begin with all 2048 RAM bytes set to zero. Separate configurations SHALL have
independent writable RAM. This deterministic initial state is an emulator convenience, not a hardware power-up claim.

#### Scenario: Construct a second memory configuration

- **WHEN** RAM in one configuration is changed and another configuration is created from the same cartridge
- **THEN** the new configuration's RAM reads as zero and later writes do not affect the first configuration

### Requirement: Map fixed NROM program data

For a supported mapper-0 configuration, CPU addresses $8000-$FFFF SHALL expose the cartridge's PRG bytes. A 16 KiB
PRG section SHALL repeat in both halves of the window; a 32 KiB section SHALL occupy the entire window in file order.

#### Scenario: Mirror a 16 KiB PRG section

- **WHEN** a cartridge contains 16384 PRG bytes with identifiable values at selected offsets
- **THEN** $8000 and $C000 read PRG offset 0, and $BFFF and $FFFF read PRG offset $3FFF

#### Scenario: Expose both halves of a 32 KiB PRG section

- **WHEN** a cartridge contains 32768 PRG bytes with different lower and upper halves
- **THEN** $8000 reads offset 0, $C000 reads offset $4000, and $FFFF reads offset $7FFF

### Requirement: Reject PRG ROM writes

Any attempt to write PRG ROM, directly or through the CPU-facing memory interface at $8000-$FFFF, SHALL raise
PermissionError without changing ROM or RAM. The CPU-facing interface SHALL propagate the ROM exception unchanged.

#### Scenario: Write into the PRG window

- **WHEN** a write targets the beginning, middle, or end of either supported PRG layout
- **THEN** PermissionError is raised and propagates through the CPU-facing interface
- **AND** subsequent reads return the original ROM bytes and RAM retains its existing values

### Requirement: Report unimplemented CPU address ranges

Reads at $2000-$3FFF except status-register aliases and reads at $4000-$7FFF SHALL raise NotImplementedError.
Writes at $4000-$7FFF SHALL raise NotImplementedError. PPU-window writes and status reads SHALL route to the PPU.
PPU read errors SHALL identify the operation and register offset; other errors SHALL identify the operation and CPU
address. Unimplemented ranges SHALL NOT act as RAM.

#### Scenario: Access an unimplemented address

- **WHEN** a read targets a non-status PPU register or $4000-$7FFF, or a write targets $4000-$7FFF
- **THEN** NotImplementedError identifies the attempted operation and PPU register offset or CPU address, respectively

#### Scenario: Write a PPU register mirror

- **WHEN** a write targets $2000-$3FFF
- **THEN** the write reaches the PPU register selected by the low three address bits

#### Scenario: Read a PPU status mirror

- **WHEN** a read targets a PPU address whose low three bits are 2
- **THEN** it returns the next status byte from the connected PPU

### Requirement: Keep unsupported cartridge configurations explicit

Memory construction SHALL support mapper 0, submapper 0, a 16 KiB or 32 KiB PRG section, and no trainer. Other mapper,
submapper, PRG-size, or trainer configurations SHALL raise NotImplementedError identifying the missing support.

#### Scenario: Connect ordinary parsed cartridge data

- **WHEN** supported cartridge metadata and PRG bytes have already been parsed
- **THEN** connected CPU memory is available without constructing a CPU, running instructions, or changing source data

#### Scenario: Reject a cartridge beyond the selected memory model

- **WHEN** construction encounters another mapper/submapper, an unsupported PRG size, or trainer data
- **THEN** NotImplementedError names that unsupported configuration rather than silently mapping it as ordinary NROM
