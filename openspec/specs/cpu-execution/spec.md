# cpu-execution Specification

## Purpose

Execute one instruction at the current CPU address through connected memory, with explicit missing behavior,
resulting-state traces, and cumulative instruction cycles for later timing work. Initial support covers CLC, SEC,
CLI, SEI, CLD, SED, CLV, and the official NOP encoding.

## Requirements

### Requirement: Fetch an instruction through connected memory

Single-instruction execution SHALL read the opcode at the current 16-bit PC through Machine's CPU byte interface.
It SHALL execute only that instruction and SHALL NOT prefetch the next instruction.
Memory-access exceptions SHALL propagate without advancing PC, adding cycles, or reporting a completed instruction.

#### Scenario: Fetch a supported opcode from mapped memory

- **WHEN** PC identifies a selected opcode in mapped RAM, a RAM mirror, or either supported PRG layout
- **THEN** one instruction is fetched through the connected memory interface and executed
- **AND** no following instruction is fetched

#### Scenario: Fetch from an unconnected address

- **WHEN** PC is $2002 and single-instruction execution is requested
- **THEN** the existing unimplemented-read exception propagates and PC and cycles remain unchanged
- **AND** no completed-instruction trace is emitted

### Requirement: Apply the common implied-instruction behavior

The supported encodings SHALL be CLC=$18, SEC=$38, CLI=$58, SEI=$78, CLD=$D8, SED=$F8, CLV=$B8, and NOP=$EA.
Each SHALL occupy one byte, advance PC by one modulo 65536, fetch no operand, and write no memory.
A, X, Y, SP, N, Z, and software B SHALL be preserved; other flag effects SHALL follow the selected instruction.

#### Scenario: Preserve unrelated CPU and memory state

- **WHEN** any selected instruction executes with known registers, flags, and memory
- **THEN** PC advances by one and its specified flag effect occurs
- **AND** every other register, flag, and memory byte remains unchanged

#### Scenario: Wrap the program counter

- **WHEN** any selected opcode is fetched at $FFFF
- **THEN** the resulting PC is $0000 without fetching an opcode there

### Requirement: Execute implied CLC

Opcode $18 SHALL execute CLC, setting the carry flag C to false.
Every other status flag SHALL remain unchanged.

#### Scenario: Assign C regardless of its previous value

- **WHEN** CLC executes with C initially false or true and known values in the other flags
- **THEN** C is false in both cases and every other flag retains its previous value

### Requirement: Execute implied SEC

Opcode $38 SHALL execute SEC, setting the carry flag C to true.
Every other status flag SHALL remain unchanged.

#### Scenario: Assign C regardless of its previous value

- **WHEN** SEC executes with C initially false or true and known values in the other flags
- **THEN** C is true in both cases and every other flag retains its previous value

### Requirement: Execute implied CLI

Opcode $58 SHALL execute CLI, setting the interrupt-disable flag I to false.
Every other status flag SHALL remain unchanged.

#### Scenario: Assign I regardless of its previous value

- **WHEN** CLI executes with I initially false or true and known values in the other flags
- **THEN** I is false in both cases and every other flag retains its previous value

### Requirement: Execute implied SEI

Opcode $78 SHALL execute SEI, setting the interrupt-disable flag I to true.
Every other status flag SHALL remain unchanged.

#### Scenario: Assign I regardless of its previous value

- **WHEN** SEI executes with I initially false or true and known values in the other flags
- **THEN** I is true in both cases and every other flag retains its previous value

### Requirement: Execute implied CLD

Opcode $D8 SHALL execute CLD, setting the decimal flag D to false.
Every other status flag SHALL remain unchanged.

#### Scenario: Assign D regardless of its previous value

- **WHEN** CLD executes with D initially false or true and known values in the other flags
- **THEN** D is false in both cases and every other flag retains its previous value

### Requirement: Execute implied SED

Opcode $F8 SHALL execute SED, setting the decimal flag D to true.
Every other status flag SHALL remain unchanged.

#### Scenario: Assign D regardless of its previous value

- **WHEN** SED executes with D initially false or true and known values in the other flags
- **THEN** D is true in both cases and every other flag retains its previous value

### Requirement: Execute implied CLV

Opcode $B8 SHALL execute CLV, setting the overflow flag V to false.
Every other status flag SHALL remain unchanged.

#### Scenario: Assign V regardless of its previous value

- **WHEN** CLV executes with V initially false or true and known values in the other flags
- **THEN** V is false in both cases and every other flag retains its previous value

### Requirement: Execute official implied NOP

Opcode $EA SHALL execute NOP, preserving all registers except the advancing PC and preserving every status flag.
It SHALL follow the common one-byte behavior and incur its normal instruction cycles.

#### Scenario: Advance without changing data or flags

- **WHEN** $EA executes with known register and flag values
- **THEN** PC advances by one, cycles increase by two, and A/X/Y/SP and all flags remain unchanged

### Requirement: Expose a cumulative instruction cycle counter

CPU SHALL expose a read-only integer cycles counter initialized to zero only on construction.
The counter SHALL accumulate without a fixed-width wrap. Repeated functional reset SHALL preserve it and add no cycles;
startup reset SHALL also add no cycles. Separate CPU instances SHALL have independent counters.

#### Scenario: Start and reset without charging instruction cycles

- **WHEN** a CPU is constructed, executes one NOP, and is then reset
- **THEN** cycles reads 0 after construction, 2 after NOP, and 2 after reset

#### Scenario: Keep independent counters

- **WHEN** one of two CPUs executes an instruction
- **THEN** only that CPU's counter increases

### Requirement: Charge cycles for completed instructions

Every completed instruction SHALL add its documented CPU cycle count.
Each of the eight selected encodings SHALL add exactly two cycles, including NOP and flag instructions whose target
flag already has the requested value. Unsupported opcodes and failed fetches SHALL add no cycles.

#### Scenario: Accumulate the selected instructions

- **WHEN** a CPU executes CLC, SEC, CLI, SEI, CLD, SED, CLV, and NOP once each
- **THEN** its counter increases by 16, with an increase of two after each completed instruction

#### Scenario: Preserve accumulated cycles after failure

- **WHEN** an unsupported opcode or failed opcode read follows completed instructions
- **THEN** cycles retains the total from those instructions without charging the failed request

### Requirement: Stop at an unsupported opcode

An opcode outside $18/$38/$58/$78/$D8/$F8/$B8/$EA SHALL raise NotImplementedError with its byte and address.
The failed instruction SHALL leave PC, other registers, flags, cycles, and memory unchanged.
It SHALL NOT be treated as an instruction that completed or silently skipped.

#### Scenario: Keep the first unsupported instruction visible

- **WHEN** SEI at $8000 and CLD at $8001 are followed by unsupported $A9 at $8002
- **THEN** two instructions complete, PC remains $8002 on failure, and cycles has increased by four
- **AND** NotImplementedError identifies $A9 at $8002 without a completed trace for it

#### Scenario: Keep unofficial NOP encodings unsupported

- **WHEN** opcode $1A is fetched
- **THEN** NotImplementedError identifies $1A and its address without changing CPU state or cycles

### Requirement: Trace completed instructions and their resulting state

With CPU DEBUG logging enabled, every completed instruction SHALL emit one line after registers, flags, PC, and cycles
have been updated. It SHALL contain the original address, instruction bytes, mnemonic, operands, and resulting
A/X/Y/SP/PC and symbolic P in NV1BDIZC order, followed by CYC=<decimal total>. Failed requests SHALL emit no completed
trace, and execution SHALL emit no extra reset event.

#### Scenario: Observe post-execution state at the original instruction address

- **WHEN** the first SEI at $8000 completes after startup with CPU DEBUG logging enabled
- **THEN** one trace identifies address 8000, byte 78, mnemonic SEI, and no operands
- **AND** its state suffix reports PC=8001, I set, and CYC=2 after execution

#### Scenario: Trace every selected mnemonic

- **WHEN** any selected opcode completes with CPU DEBUG logging enabled
- **THEN** one line reports that opcode's actual mnemonic and resulting state, including NOP

### Requirement: Align instruction trace columns

Trace fields SHALL use ASCII spaces: a 4-digit zero-padded uppercase hex address, 3 spaces, an 8-character byte field,
3 spaces, a 3-character uppercase mnemonic, 1 space, a 20-character operand field, and 1 space before state.
Bytes SHALL be uppercase two-digit hex separated by single spaces. Byte, mnemonic, and operand fields SHALL be
left-aligned and space-padded; absent operands and unused byte slots SHALL stay blank. State SHALL start at column 44.

#### Scenario: Align metadata for one-byte, two-byte, and three-byte instructions

- **WHEN** trace formatting receives instruction bytes 78, A9 10, or 4C 00 C0 and their mnemonic/operand text
- **THEN** the byte field starts at column 8, mnemonic at 19, operands at 23, and state at 44 in every formatted line
- **AND** all supplied bytes appear without zero-filling unused slots or shifting later fields

#### Scenario: Leave the operand field blank for implied addressing

- **WHEN** any of the eight supported implied instructions is traced
- **THEN** all 20 operand-field characters are spaces and the state begins at the same fixed column

### Requirement: Trace fetched bytes without additional memory access

Instruction traces SHALL use the bytes captured during instruction fetch and operand decoding.
Rendering a trace SHALL NOT reread instruction memory or read extra bytes to fill the display field.
The original instruction address SHALL remain distinct from the resulting PC, including after wraparound.

#### Scenario: Render an instruction next to unconnected memory

- **WHEN** SEI at $1FFF completes and advances PC to unconnected address $2000
- **THEN** its trace shows the original byte 78 and resulting PC=2000 without accessing $2000 or $2001 for formatting

#### Scenario: Render supplied metadata without executing it

- **WHEN** supplied two-byte or three-byte instruction metadata is rendered
- **THEN** formatting performs no instruction fetch or execution and leaves registers, flags, and cycles unchanged
