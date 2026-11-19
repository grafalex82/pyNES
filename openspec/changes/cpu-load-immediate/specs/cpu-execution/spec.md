## ADDED Requirements

### Requirement: Load immediate into a CPU register

LDA ($A9), LDX ($A2), and LDY ($A0) SHALL load the next byte into A, X, and Y respectively. Each SHALL set N
from bit 7, set Z exactly when the loaded value is zero, preserve other registers and flags, and add two cycles.

#### Scenario: Load each boundary value

- **WHEN** each opcode loads $00, $7F, $80, or $FF from the next instruction byte
- **THEN** its destination contains that byte, N and Z reflect the result, PC advances by two modulo 65536,
  and all unrelated state is unchanged

### Requirement: Store registers using absolute addressing

STA ($8D), STX ($8E), and STY ($8C) SHALL write A, X, and Y respectively to the absolute address encoded low byte first.
Each SHALL preserve registers and flags other than advancing PC by three modulo 65536 and SHALL add four cycles.

#### Scenario: Store each register through memory routing

- **WHEN** each opcode stores a distinctive register value at a writable RAM address
- **THEN** the addressed byte becomes that value, unrelated memory and CPU state are preserved, and four cycles accrue

#### Scenario: Propagate a device write error

- **WHEN** a store targets an unconnected address or read-only ROM
- **THEN** the device error propagates and no completed instruction trace or cycles are added

### Requirement: Transfer between X and the stack pointer

TXS ($9A) SHALL copy X to SP, advance PC by one modulo 65536, and add two cycles. It SHALL preserve X,
all other registers, every status flag, and memory.
TSX ($BA) SHALL copy SP to X, set N from bit 7 and Z when the result is zero, advance PC by one modulo 65536,
and add two cycles. It SHALL preserve SP, all other registers, flags other than N/Z, and memory.

#### Scenario: Transfer boundary values

- **WHEN** TXS executes with X set to $00 or $FF
- **THEN** SP equals X, flags remain unchanged, and the instruction adds two cycles

#### Scenario: Transfer stack pointer to X

- **WHEN** TSX executes with SP set to $00, $7F, $80, or $FF
- **THEN** X equals SP, N and Z reflect the result, and the instruction adds two cycles

### Requirement: Transfer between the accumulator and index registers

TXA ($8A), TYA ($98), TAX ($AA), and TAY ($A8) SHALL copy X to A, Y to A, A to X, and A to Y respectively.
Each SHALL set N from bit 7 and Z when the result is zero, preserve other flags and registers, advance PC by one,
and add two cycles. Memory SHALL remain unchanged.

#### Scenario: Transfer each boundary value

- **WHEN** each instruction executes with its source set to $00, $7F, $80, or $FF
- **THEN** its destination equals the source, N and Z reflect the result, and the instruction adds two cycles

### Requirement: Load a register using absolute addressing

LDA ($AD), LDX ($AE), and LDY ($AC) SHALL read the absolute address encoded low byte first into A, X, and Y
respectively. Each SHALL set N from bit 7, set Z exactly when the value is zero, preserve other state except PC and
cycles, advance PC by three modulo 65536, and add four cycles.

#### Scenario: Load each value from mapped memory

- **WHEN** each opcode reads $00, $7F, $80, or $FF from mapped RAM or ROM
- **THEN** its destination, N, Z, PC, and cycles reflect the loaded byte and unrelated state is preserved

#### Scenario: Read a memory-mapped device

- **WHEN** an absolute load addresses a connected PPU register
- **THEN** it performs one read through Machine and uses that single returned byte for the register and trace

### Requirement: Branch when negative is clear

BPL ($10) SHALL read a signed 8-bit relative displacement and branch from the PC after the operand if N is clear.
PC arithmetic SHALL wrap modulo 65536. The instruction SHALL preserve registers other than PC and all flags.
It SHALL add two cycles, plus one if taken, plus one more if a taken branch crosses a page.

#### Scenario: Branch backward when N is clear

- **WHEN** BPL $FB is at $800D with N clear
- **THEN** PC becomes $800A, all flags remain unchanged, and three cycles accrue

#### Scenario: Do not branch when N is set

- **WHEN** BPL executes with N set
- **THEN** PC advances past the operand and two cycles accrue

#### Scenario: Cross a page or wrap the address space

- **WHEN** a taken branch crosses a page boundary, including across $FFFF and $0000
- **THEN** PC reaches the signed relative target modulo 65536 and four cycles accrue

### Requirement: Decrement an index register

DEX ($CA) SHALL decrement X and DEY ($88) SHALL decrement Y modulo 256. Each SHALL set N from result bit 7,
set Z exactly when the result is zero, preserve other registers and flags, advance PC by one, and add two cycles.

#### Scenario: Decrement each boundary value

- **WHEN** DEX or DEY executes with its selected register at $00, $01, or $80
- **THEN** the result is $FF, $00, or $7F respectively and N and Z reflect the result

## MODIFIED Requirements

### Requirement: Stop at an unsupported opcode

An opcode without an implemented handler SHALL raise NotImplementedError with its byte and address.
The failed instruction SHALL leave PC, other registers, flags, cycles, and memory unchanged.
It SHALL NOT be treated as an instruction that completed or silently skipped.

#### Scenario: Keep the first unsupported instruction visible

- **WHEN** SEI at $8000 and CLD at $8001 are followed by unsupported $02 at $8002
- **THEN** two instructions complete, PC remains $8002 on failure, and cycles has increased by four
- **AND** NotImplementedError identifies $02 at $8002 without a completed trace for it

#### Scenario: Keep unofficial NOP encodings unsupported

- **WHEN** opcode $1A is fetched
- **THEN** NotImplementedError identifies $1A and its address without changing CPU state or cycles
