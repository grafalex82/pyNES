## Purpose

Provide an incremental CPU-facing video register boundary for educational NES execution.

## ADDED Requirements

### Requirement: Accept PPU register writes

The PPU SHALL retain the last byte written independently for each of eight register offsets. CPU addresses
$2000-$3FFF SHALL select offset (address - $2000) modulo 8. Retention SHALL NOT implement any register effects.

#### Scenario: Write through register mirrors

- **WHEN** distinct values are written to a register and its mirrors
- **THEN** the register's retained byte equals the last written value without changing the other seven retained bytes

#### Scenario: Write the status offset

- **WHEN** a byte is written to $2002 or its mirrors
- **THEN** the write is accepted and retained like other offsets, without implementing PPUSTATUS hardware behavior

### Requirement: Return alternating status values

Consecutive CPU reads of PPUSTATUS at $2002 or any mirror SHALL return $00 and $80 alternately, starting with $00
for each new PPU. A read through any alias SHALL advance the same per-device sequence.

#### Scenario: Read successive status values through mirrors

- **WHEN** a new PPU is read at $2002, $200A, $3FFA, and $2002
- **THEN** the returned bytes are $00, $80, $00, and $80 in order

#### Scenario: Keep status sequence independent

- **WHEN** one PPU is read or any register is written and a second new PPU is read
- **THEN** the second PPU returns $00 on its first status read
