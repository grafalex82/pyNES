# PPU Memory

## Purpose

Provide the PPU with its own video address space backed by cartridge CHR ROM, console VRAM, and palette RAM.

## ADDED Requirements

### Requirement: Connect fixed NROM CHR ROM

For a supported mapper-0 cartridge, Machine SHALL connect its 8 KiB CHR ROM to PPU addresses $0000-$1FFF in file
order. CHR writes SHALL raise PermissionError and preserve the bytes.

#### Scenario: Read both pattern tables

- **WHEN** the two 4 KiB halves contain distinct bytes at their boundaries
- **THEN** reads at $0000, $0FFF, $1000, and $1FFF return the corresponding cartridge bytes
- **AND** a rejected write leaves the addressed byte intact

### Requirement: Map the two physical nametables

The PPU SHALL address two writable 1 KiB VRAM pages through four logical nametables at $2000, $2400, $2800,
and $2C00. Horizontal mirroring SHALL map them to pages 0, 0, 1, 1 and vertical mirroring to 0, 1, 0, 1.
Addresses $3000-$3EFF SHALL alias $2000-$2EFF.

#### Scenario: Write through a nametable alias

- **WHEN** a PPU writes a byte in each physical page using either supported mirroring arrangement
- **THEN** every alias of each byte returns the same value and the two physical pages retain distinct values
- **AND** writes to that VRAM are independent of CPU RAM and other Machine instances

### Requirement: Store and mirror palette colors

The PPU SHALL store six-bit colors at $3F00-$3F1F and mirror that range every 32 bytes through $3FFF.
Entries $3F10, $3F14, $3F18, and $3F1C SHALL alias $3F00, $3F04, $3F08, and $3F0C, respectively.

#### Scenario: Access a palette color through both kinds of mirror

- **WHEN** $E1 is written to $3F30
- **THEN** reads at $3F00, $3F10, and $3F20 return $21
- **AND** adjacent entries retain their previous values

### Requirement: Diagnose unsupported video memory configurations

Video access for unsupported CHR configurations or mirroring SHALL raise NotImplementedError naming that
configuration. CPU-only construction for existing supported PRG configurations SHALL still be possible.

#### Scenario: Distinguish absent CHR ROM from a valid pattern table

- **WHEN** a supported synthetic PRG cartridge without CHR ROM is used for CPU execution
- **THEN** CPU execution remains available
- **AND** accessing its CHR memory reports unsupported CHR RAM
