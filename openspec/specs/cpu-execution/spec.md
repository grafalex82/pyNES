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

- **WHEN** PC is $4000 and single-instruction execution is requested
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

### Requirement: Branch on a status flag

BEQ ($F0)/BNE ($D0) SHALL branch if Z is set/clear; BPL ($10)/BMI ($30) if N is clear/set;
BCC ($90)/BCS ($B0) if C is clear/set; BVC ($50)/BVS ($70) if V is clear/set.
Each SHALL apply a signed 8-bit displacement to the post-operand PC when its condition holds, wrapping at 16 bits.
All flags and registers except PC SHALL be preserved. The cost SHALL be two cycles, plus one if taken and one more
if a taken branch crosses a page.

#### Scenario: Branch backward when N is clear

- **WHEN** BPL $FB is at $800D with N clear
- **THEN** PC becomes $800A, all flags remain unchanged, and three cycles accrue

#### Scenario: Check each branch condition

- **WHEN** each branch executes with its tested flag set and clear
- **THEN** it branches only for its specified condition; otherwise PC advances past the operand and two cycles accrue

#### Scenario: Cross a page

- **WHEN** a taken branch crosses a page boundary
- **THEN** PC reaches the signed relative target and four cycles accrue

### Requirement: Increment or decrement an index register

INX ($E8) and INY ($C8) SHALL increment X and Y; DEX ($CA) and DEY ($88) SHALL decrement X and Y, modulo 256.
Each SHALL set N from result bit 7, set Z exactly when the result is zero, preserve other registers and flags,
advance PC by one, and add two cycles.

#### Scenario: Increment each boundary value

- **WHEN** INX or INY executes with its selected register at $00, $7F, or $FF
- **THEN** the result is $01, $80, or $00 respectively and N and Z reflect the result

#### Scenario: Decrement each boundary value

- **WHEN** DEX or DEY executes with its selected register at $00, $01, or $80
- **THEN** the result is $FF, $00, or $7F respectively and N and Z reflect the result

### Requirement: Execute INC using zero-page addressing

Opcode $E6 SHALL zero-extend its one-byte operand to obtain a zero-page address and read its byte through Machine. It
SHALL increment the byte modulo 256 and set N/Z from the result. It SHALL write the original byte and then the modified
byte through Machine at that address. It SHALL advance PC by two and add 5 nominal cycles. All status flags other than
N/Z SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $FF
- **THEN** the result is $00, N=0, and Z=1

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Address both ends of zero page
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is respectively $0000 or $00FF

### Requirement: Execute DEC using zero-page addressing

Opcode $C6 SHALL zero-extend its one-byte operand to obtain a zero-page address and read its byte through Machine. It
SHALL decrement the byte modulo 256 and set N/Z from the result. It SHALL write the original byte and then the modified
byte through Machine at that address. It SHALL advance PC by two and add 5 nominal cycles. All status flags other than
N/Z SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $00
- **THEN** the result is $FF, N=1, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Address both ends of zero page
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is respectively $0000 or $00FF

### Requirement: Execute BIT using zero-page addressing

Opcode $24 SHALL zero-extend its one-byte operand to obtain a zero-page address and read its byte through Machine. It
SHALL set Z if A AND the byte is zero and set N and V from bits 7 and 6 of the byte, without changing A. It SHALL
advance PC by two and add 3 nominal cycles. All status flags other than N/V/Z SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$40 and addressed memory contains $80
- **THEN** A remains $40, Z=1, N=1, and V=0

#### Scenario: Address both ends of zero page
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is respectively $0000 or $00FF

#### Scenario: Test a matching bit independently of N/V
- **WHEN** A=$40 and addressed memory contains $40
- **THEN** A remains $40, Z=0, N=0, and V=1

### Requirement: Execute BIT using absolute addressing

Opcode $2C SHALL use its little-endian 16-bit operand as the effective address and read the byte through Machine.
It SHALL set Z if A AND the byte is zero and set N and V from bits 7 and 6 of the byte, without changing A. It SHALL
advance PC by three and add four nominal cycles. All status flags other than N/V/Z SHALL remain unchanged.

#### Scenario: Test nonmatching bits
- **WHEN** A=$40 and addressed memory contains $80
- **THEN** A remains $40, Z=1, N=1, and V=0

#### Scenario: Test a matching bit independently of N/V
- **WHEN** A=$40 and addressed memory contains $40
- **THEN** A remains $40, Z=0, N=0, and V=1

#### Scenario: Decode the address
- **WHEN** the operand bytes are $56 followed by $04
- **THEN** the byte is read from $0456 through Machine

### Requirement: Execute CMP using zero-page addressing

Opcode $C5 SHALL zero-extend its one-byte operand to obtain a zero-page address and read its byte through Machine. It
SHALL compare A with the byte without storing the difference; set C if A is greater than or equal to the byte, Z on
equality, and N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add 3 nominal cycles. All status
flags other than C/N/Z SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$40 and addressed memory contains $40
- **THEN** C=1, Z=1, and N=0

#### Scenario: Address both ends of zero page
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is respectively $0000 or $00FF

### Requirement: Execute CPX using zero-page addressing

Opcode $E4 SHALL zero-extend its one-byte operand to obtain a zero-page address and read its byte through Machine. It
SHALL compare X with the byte without storing the difference; set C if X is greater than or equal to the byte, Z on
equality, and N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add 3 nominal cycles. All status
flags other than C/N/Z SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** X=$40 and addressed memory contains $40
- **THEN** C=1, Z=1, and N=0

#### Scenario: Address both ends of zero page
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is respectively $0000 or $00FF

### Requirement: Execute CPY using zero-page addressing

Opcode $C4 SHALL zero-extend its one-byte operand to obtain a zero-page address and read its byte through Machine. It
SHALL compare Y with the byte without storing the difference; set C if Y is greater than or equal to the byte, Z on
equality, and N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add 3 nominal cycles. All status
flags other than C/N/Z SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** Y=$40 and addressed memory contains $40
- **THEN** C=1, Z=1, and N=0

#### Scenario: Address both ends of zero page
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is respectively $0000 or $00FF

### Requirement: Execute INC using zero-page,X addressing

Opcode $F6 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL increment the byte modulo 256 and set N/Z from the result. It SHALL write the original byte and then
the modified byte through Machine at that address. It SHALL advance PC by two and add 6 nominal cycles. All status flags
other than N/Z SHALL remain unchanged. The functional model omits the discarded read at the unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $FF
- **THEN** the result is $00, N=0, and Z=1

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 6 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 6 nominal cycles

### Requirement: Execute DEC using zero-page,X addressing

Opcode $D6 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL decrement the byte modulo 256 and set N/Z from the result. It SHALL write the original byte and then
the modified byte through Machine at that address. It SHALL advance PC by two and add 6 nominal cycles. All status flags
other than N/Z SHALL remain unchanged. The functional model omits the discarded read at the unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $00
- **THEN** the result is $FF, N=1, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 6 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 6 nominal cycles

### Requirement: Execute CMP using zero-page,X addressing

Opcode $D5 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL compare A with the byte without storing the difference; set C if A is greater than or equal to the
byte, Z on equality, and N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add 4 nominal cycles.
All status flags other than C/N/Z SHALL remain unchanged. The functional model omits the discarded read at the unindexed
zero-page address.

#### Scenario: Apply the operation
- **WHEN** A=$40 and addressed memory contains $40
- **THEN** C=1, Z=1, and N=0

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 4 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 4 nominal cycles

### Requirement: Execute ADC using zero-page,X addressing

Opcode $75 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL add the byte and incoming C to A using binary arithmetic regardless of D, updating A and C/V/N/Z. It
SHALL advance PC by two and add 4 nominal cycles. All status flags other than C/V/N/Z SHALL remain unchanged. The
functional model omits the discarded read at the unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** A=$7F, C=0, and addressed memory contains $01
- **THEN** A=$80, C=0, V=1, N=1, and Z=0

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 4 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 4 nominal cycles

### Requirement: Execute SBC using zero-page,X addressing

Opcode $F5 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL subtract the byte and inverse of incoming C from A using binary arithmetic regardless of D, updating A
and C/V/N/Z. It SHALL advance PC by two and add 4 nominal cycles. All status flags other than C/V/N/Z SHALL remain
unchanged. The functional model omits the discarded read at the unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** A=$00, C=1, and addressed memory contains $01
- **THEN** A=$FF, C=0, V=0, N=1, and Z=0

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 4 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 4 nominal cycles

### Requirement: Execute AND using zero-page,X addressing

Opcode $35 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL combine A with the byte using bitwise AND, updating A and N/Z. It SHALL advance PC by two and add 4
nominal cycles. All status flags other than N/Z SHALL remain unchanged. The functional model omits the discarded read at
the unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** A=$F0 and addressed memory contains $0F
- **THEN** A=$00, N=0, and Z=1

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 4 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 4 nominal cycles

### Requirement: Execute ORA using zero-page,X addressing

Opcode $15 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL combine A with the byte using bitwise OR, updating A and N/Z. It SHALL advance PC by two and add 4
nominal cycles. All status flags other than N/Z SHALL remain unchanged. The functional model omits the discarded read at
the unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** A=$80 and addressed memory contains $01
- **THEN** A=$81, N=1, and Z=0

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 4 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 4 nominal cycles

### Requirement: Execute EOR using zero-page,X addressing

Opcode $55 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL combine A with the byte using bitwise exclusive OR, updating A and N/Z. It SHALL advance PC by two and
add 4 nominal cycles. All status flags other than N/Z SHALL remain unchanged. The functional model omits the discarded
read at the unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** A=$FF and addressed memory contains $0F
- **THEN** A=$F0, N=1, and Z=0

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 4 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 4 nominal cycles

### Requirement: Execute ASL using zero-page,X addressing

Opcode $16 SHALL add X to its operand modulo 256 and read the zero-page byte through Machine. It SHALL shift the byte
left, set C from bit 7, insert zero into bit 0, and set N/Z from the result. It SHALL write the original byte then the
result through Machine. It SHALL advance PC by two, add six cycles, and preserve other flags. The functional model omits
the discarded read at the unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $81
- **THEN** the result is $02, C=1, N=0, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 6 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 6 nominal cycles

### Requirement: Execute LSR using zero-page,X addressing

Opcode $56 SHALL add X to its operand modulo 256 and read the zero-page byte through Machine. It SHALL shift the byte
right, set C from bit 0, insert zero into bit 7, and set N/Z from the result. It SHALL write the original byte then the
result through Machine. It SHALL advance PC by two, add six cycles, and preserve other flags. The functional model omits
the discarded read at the unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $01
- **THEN** the result is $00, C=1, N=0, and Z=1

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 6 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 6 nominal cycles

### Requirement: Execute ROL using zero-page,X addressing

Opcode $36 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL rotate the byte left through incoming C, moving bit 7 to C, and update C/N/Z. It SHALL write the
original byte and then the modified byte through Machine at that address. It SHALL advance PC by two and add 6 nominal
cycles. All status flags other than C/N/Z SHALL remain unchanged. The functional model omits the discarded read at the
unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $80 and C=1
- **THEN** the result is $01, C=1, N=0, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 6 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 6 nominal cycles

### Requirement: Execute ROR using zero-page,X addressing

Opcode $76 SHALL add X to its one-byte operand modulo 256 to obtain a zero-page address and read its byte through
Machine. It SHALL rotate the byte right through incoming C, moving bit 0 to C, and update C/N/Z. It SHALL write the
original byte and then the modified byte through Machine at that address. It SHALL advance PC by two and add 6 nominal
cycles. All status flags other than C/N/Z SHALL remain unchanged. The functional model omits the discarded read at the
unindexed zero-page address.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $01 and C=1
- **THEN** the result is $80, C=1, N=1, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the effective address is $0010 and the instruction takes 6 nominal cycles

#### Scenario: Index within zero page
- **WHEN** the operand is $20 and X=$04
- **THEN** the effective address is $0024 and the instruction takes 6 nominal cycles

### Requirement: Execute CMP using absolute addressing

Opcode $CD SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL compare A with the fetched byte without storing the difference; C SHALL indicate A >= byte, Z
equality, and N bit 7 of the eight-bit difference. It SHALL advance PC by three and add four nominal cycles. All other
status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$40 and addressed memory contains $40
- **THEN** C=1, Z=1, and N=0

### Requirement: Execute CMP using absolute,X addressing

Opcode $DD SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL compare A with the fetched byte without storing the difference; C SHALL indicate A >= byte, Z equality, and N bit
7 of the eight-bit difference. It SHALL advance PC by three and add four nominal cycles plus one on page crossing. The
functional model omits the provisional read on a page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$40 and addressed memory contains $40
- **THEN** C=1, Z=1, and N=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute CMP using absolute,Y addressing

Opcode $D9 SHALL add Y to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL compare A with the fetched byte without storing the difference; C SHALL indicate A >= byte, Z equality, and N bit
7 of the eight-bit difference. It SHALL advance PC by three and add four nominal cycles plus one on page crossing. The
functional model omits the provisional read on a page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$40 and addressed memory contains $40
- **THEN** C=1, Z=1, and N=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and Y=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and Y=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and Y=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute CPX using absolute addressing

Opcode $EC SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL compare X with the fetched byte without storing the difference; C SHALL indicate X >= byte, Z
equality, and N bit 7 of the eight-bit difference. It SHALL advance PC by three and add four nominal cycles. All other
status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** X=$40 and addressed memory contains $40
- **THEN** C=1, Z=1, and N=0

### Requirement: Execute CPY using absolute addressing

Opcode $CC SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL compare Y with the fetched byte without storing the difference; C SHALL indicate Y >= byte, Z
equality, and N bit 7 of the eight-bit difference. It SHALL advance PC by three and add four nominal cycles. All other
status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** Y=$40 and addressed memory contains $40
- **THEN** C=1, Z=1, and N=0

### Requirement: Execute ADC using absolute addressing

Opcode $6D SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL add the fetched byte and incoming C to A using binary arithmetic regardless of D, updating A and
C/V/N/Z. It SHALL advance PC by three and add four nominal cycles. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$7F, C=0, and addressed memory contains $01
- **THEN** A=$80, C=0, V=1, N=1, and Z=0

### Requirement: Execute ADC using absolute,X addressing

Opcode $7D SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL add the fetched byte and incoming C to A using binary arithmetic regardless of D, updating A and C/V/N/Z. It SHALL
advance PC by three and add four nominal cycles plus one on page crossing. The functional model omits the provisional
read on a page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$7F, C=0, and addressed memory contains $01
- **THEN** A=$80, C=0, V=1, N=1, and Z=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute ADC using absolute,Y addressing

Opcode $79 SHALL add Y to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL add the fetched byte and incoming C to A using binary arithmetic regardless of D, updating A and C/V/N/Z. It SHALL
advance PC by three and add four nominal cycles plus one on page crossing. The functional model omits the provisional
read on a page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$7F, C=0, and addressed memory contains $01
- **THEN** A=$80, C=0, V=1, N=1, and Z=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and Y=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and Y=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and Y=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute SBC using absolute addressing

Opcode $ED SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL subtract the fetched byte and inverse of incoming C from A using binary arithmetic regardless of D,
updating A and C/V/N/Z. It SHALL advance PC by three and add four nominal cycles. All other status flags SHALL remain
unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$00, C=1, and addressed memory contains $01
- **THEN** A=$FF, C=0, V=0, N=1, and Z=0

### Requirement: Execute SBC using absolute,X addressing

Opcode $FD SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL subtract the fetched byte and inverse of incoming C from A using binary arithmetic regardless of D, updating A and
C/V/N/Z. It SHALL advance PC by three and add four nominal cycles plus one on page crossing. The functional model omits
the provisional read on a page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$00, C=1, and addressed memory contains $01
- **THEN** A=$FF, C=0, V=0, N=1, and Z=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute SBC using absolute,Y addressing

Opcode $F9 SHALL add Y to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL subtract the fetched byte and inverse of incoming C from A using binary arithmetic regardless of D, updating A and
C/V/N/Z. It SHALL advance PC by three and add four nominal cycles plus one on page crossing. The functional model omits
the provisional read on a page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$00, C=1, and addressed memory contains $01
- **THEN** A=$FF, C=0, V=0, N=1, and Z=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and Y=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and Y=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and Y=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute AND using absolute addressing

Opcode $2D SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL combine A with the fetched byte using bitwise AND, updating A and N/Z. It SHALL advance PC by three
and add four nominal cycles. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$F0 and addressed memory contains $0F
- **THEN** A=$00, N=0, and Z=1

### Requirement: Execute AND using absolute,X addressing

Opcode $3D SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL combine A with the fetched byte using bitwise AND, updating A and N/Z. It SHALL advance PC by three and add four
nominal cycles plus one on page crossing. The functional model omits the provisional read on a page crossing. All other
status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$F0 and addressed memory contains $0F
- **THEN** A=$00, N=0, and Z=1

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute AND using absolute,Y addressing

Opcode $39 SHALL add Y to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL combine A with the fetched byte using bitwise AND, updating A and N/Z. It SHALL advance PC by three and add four
nominal cycles plus one on page crossing. The functional model omits the provisional read on a page crossing. All other
status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$F0 and addressed memory contains $0F
- **THEN** A=$00, N=0, and Z=1

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and Y=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and Y=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and Y=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute ORA using absolute addressing

Opcode $0D SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL combine A with the fetched byte using bitwise OR, updating A and N/Z. It SHALL advance PC by three and
add four nominal cycles. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$80 and addressed memory contains $01
- **THEN** A=$81, N=1, and Z=0

### Requirement: Execute ORA using absolute,X addressing

Opcode $1D SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL combine A with the fetched byte using bitwise OR, updating A and N/Z. It SHALL advance PC by three and add four
nominal cycles plus one on page crossing. The functional model omits the provisional read on a page crossing. All other
status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$80 and addressed memory contains $01
- **THEN** A=$81, N=1, and Z=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute ORA using absolute,Y addressing

Opcode $19 SHALL add Y to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL combine A with the fetched byte using bitwise OR, updating A and N/Z. It SHALL advance PC by three and add four
nominal cycles plus one on page crossing. The functional model omits the provisional read on a page crossing. All other
status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$80 and addressed memory contains $01
- **THEN** A=$81, N=1, and Z=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and Y=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and Y=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and Y=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute EOR using absolute addressing

Opcode $4D SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL combine A with the fetched byte using bitwise exclusive OR, updating A and N/Z. It SHALL advance PC by
three and add four nominal cycles. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$FF and addressed memory contains $0F
- **THEN** A=$F0, N=1, and Z=0

### Requirement: Execute EOR using absolute,X addressing

Opcode $5D SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL combine A with the fetched byte using bitwise exclusive OR, updating A and N/Z. It SHALL advance PC by three and
add four nominal cycles plus one on page crossing. The functional model omits the provisional read on a page crossing.
All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$FF and addressed memory contains $0F
- **THEN** A=$F0, N=1, and Z=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute EOR using absolute,Y addressing

Opcode $59 SHALL add Y to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL combine A with the fetched byte using bitwise exclusive OR, updating A and N/Z. It SHALL advance PC by three and
add four nominal cycles plus one on page crossing. The functional model omits the provisional read on a page crossing.
All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** A=$FF and addressed memory contains $0F
- **THEN** A=$F0, N=1, and Z=0

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and Y=$01
- **THEN** the effective address is $1300 and the instruction takes 5 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and Y=$01
- **THEN** the effective address is $0000 and the instruction takes 5 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and Y=$01
- **THEN** the effective address is $1201 and the instruction takes four nominal cycles

### Requirement: Execute ASL using absolute addressing

Opcode $0E SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL shift the fetched byte left, moving bit 7 to C and setting bit 0 to zero, and update C/N/Z. It SHALL
write the original byte and then the modified byte through Machine, advance PC by three, and add 6 nominal cycles. All
other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $81
- **THEN** the written result is $02, C=1, N=0, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

### Requirement: Execute ASL using absolute,X addressing

Opcode $1E SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL shift the fetched byte left, moving bit 7 to C and setting bit 0 to zero, and update C/N/Z. It SHALL write the
original byte and then the modified byte through Machine, advance PC by three, and add 7 nominal cycles. The functional
model omits the provisional indexed read regardless of page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $81
- **THEN** the written result is $02, C=1, N=0, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 7 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 7 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes seven nominal cycles

### Requirement: Execute LSR using absolute addressing

Opcode $4E SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL shift the fetched byte right, moving bit 0 to C and setting bit 7 to zero, and update C/N/Z. It SHALL
write the original byte and then the modified byte through Machine, advance PC by three, and add 6 nominal cycles. All
other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $01
- **THEN** the written result is $00, C=1, N=0, and Z=1

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

### Requirement: Execute LSR using absolute,X addressing

Opcode $5E SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL shift the fetched byte right, moving bit 0 to C and setting bit 7 to zero, and update C/N/Z. It SHALL write the
original byte and then the modified byte through Machine, advance PC by three, and add 7 nominal cycles. The functional
model omits the provisional indexed read regardless of page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $01
- **THEN** the written result is $00, C=1, N=0, and Z=1

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 7 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 7 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes seven nominal cycles

### Requirement: Execute ROL using absolute addressing

Opcode $2E SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL rotate the fetched byte left through incoming C, moving bit 7 to C, and update C/N/Z. It SHALL write
the original byte and then the modified byte through Machine, advance PC by three, and add 6 nominal cycles. All other
status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $80 and C=1
- **THEN** the written result is $01, C=1, N=0, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

### Requirement: Execute ROL using absolute,X addressing

Opcode $3E SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL rotate the fetched byte left through incoming C, moving bit 7 to C, and update C/N/Z. It SHALL write the original
byte and then the modified byte through Machine, advance PC by three, and add 7 nominal cycles. The functional model
omits the provisional indexed read regardless of page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $80 and C=1
- **THEN** the written result is $01, C=1, N=0, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 7 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 7 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes seven nominal cycles

### Requirement: Execute ROR using absolute addressing

Opcode $6E SHALL use its little-endian 16-bit operand as the effective address and read the addressed byte through
Machine. It SHALL rotate the fetched byte right through incoming C, moving bit 0 to C, and update C/N/Z. It SHALL write
the original byte and then the modified byte through Machine, advance PC by three, and add 6 nominal cycles. All other
status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $01 and C=1
- **THEN** the written result is $80, C=1, N=1, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

### Requirement: Execute ROR using absolute,X addressing

Opcode $7E SHALL add X to the little-endian 16-bit operand modulo 65536 and read the addressed byte through Machine. It
SHALL rotate the fetched byte right through incoming C, moving bit 0 to C, and update C/N/Z. It SHALL write the original
byte and then the modified byte through Machine, advance PC by three, and add 7 nominal cycles. The functional model
omits the provisional indexed read regardless of page crossing. All other status flags SHALL remain unchanged.

#### Scenario: Apply the operation
- **WHEN** addressed memory contains $01 and C=1
- **THEN** the written result is $80, C=1, N=1, and Z=0

#### Scenario: Preserve the memory write sequence
- **WHEN** the addressed byte is read and modified
- **THEN** Machine receives the original byte followed by the modified byte at the effective address

#### Scenario: Index across an address boundary
- **WHEN** the base address is $12FF and X=$01
- **THEN** the effective address is $1300 and the instruction takes 7 nominal cycles

#### Scenario: Wrap the effective address
- **WHEN** the base address is $FFFF and X=$01
- **THEN** the effective address is $0000 and the instruction takes 7 nominal cycles

#### Scenario: Index without crossing a page
- **WHEN** the base address is $1200 and X=$01
- **THEN** the effective address is $1201 and the instruction takes seven nominal cycles

### Requirement: Execute STA using zero-page,X addressing

Opcode $95 SHALL add X to its one-byte operand modulo 256 and write A through Machine to that zero-page address. It
SHALL advance PC by two, add four nominal cycles, and preserve all other registers and all flags.

#### Scenario: Index within zero page
- **WHEN** A=$A5, the operand is $20, and X=$04
- **THEN** $A5 is written to $0024

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the write targets $0010

### Requirement: Execute STX using zero-page,Y addressing

Opcode $96 SHALL add Y to its one-byte operand modulo 256 and write X through Machine to that zero-page address. It
SHALL advance PC by two, add four nominal cycles, and preserve all other registers and all flags.

#### Scenario: Index within zero page
- **WHEN** X=$A5, the operand is $20, and Y=$04
- **THEN** $A5 is written to $0024

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and Y=$20
- **THEN** the write targets $0010

### Requirement: Execute STY using zero-page,X addressing

Opcode $94 SHALL add X to its one-byte operand modulo 256 and write Y through Machine to that zero-page address. It
SHALL advance PC by two, add four nominal cycles, and preserve all other registers and all flags.

#### Scenario: Index within zero page
- **WHEN** Y=$A5, the operand is $20, and X=$04
- **THEN** $A5 is written to $0024

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0 and X=$20
- **THEN** the write targets $0010

### Requirement: Execute LDA using zero-page,X addressing

Opcode $B5 SHALL add X to its one-byte operand modulo 256 and read that zero-page address through Machine into A. It
SHALL set N/Z from the loaded byte, advance PC by two, add four nominal cycles, and preserve other registers and flags.

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0, X=$20, and $0010 contains $80
- **THEN** A=$80, N=1, and Z=0

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** A holds the value, N equals bit 7, and Z is set only for $00

### Requirement: Execute LDX using zero-page,Y addressing

Opcode $B6 SHALL add Y to its one-byte operand modulo 256 and read that zero-page address through Machine into X. It
SHALL set N/Z from the loaded byte, advance PC by two, add four nominal cycles, and preserve other registers and flags.

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0, Y=$20, and $0010 contains $80
- **THEN** X=$80, N=1, and Z=0

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** X holds the value, N equals bit 7, and Z is set only for $00

### Requirement: Execute LDY using zero-page,X addressing

Opcode $B4 SHALL add X to its one-byte operand modulo 256 and read that zero-page address through Machine into Y. It
SHALL set N/Z from the loaded byte, advance PC by two, add four nominal cycles, and preserve other registers and flags.

#### Scenario: Wrap within zero page
- **WHEN** the operand is $F0, X=$20, and $0010 contains $80
- **THEN** Y=$80, N=1, and Z=0

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** Y holds the value, N equals bit 7, and Z is set only for $00

### Requirement: Execute ADC using zero-page addressing

Opcode $65 SHALL read the zero-extended one-byte address through Machine, add its value and incoming C to A in binary,
and update A and C/V/N/Z using NES arithmetic rules. It SHALL preserve D without using decimal arithmetic, preserve
other registers and flags, advance PC by two, and add three nominal cycles.

#### Scenario: Carry out of the byte
- **WHEN** A=$FF, the addressed byte is $00, and C=1
- **THEN** A=$00, C=1, V=0, N=0, and Z=1

#### Scenario: Signed overflow and decimal flag
- **WHEN** A=$7F, the addressed byte is $01, C=0, and D=1
- **THEN** A=$80, C=0, V=1, N=1, Z=0, and D remains set

### Requirement: Execute SBC using zero-page addressing

Opcode $E5 SHALL read the zero-extended one-byte address through Machine, subtract its value and inverse incoming C from
A in binary, and update A and C/V/N/Z using NES arithmetic rules. It SHALL preserve D without using decimal arithmetic,
preserve other registers and flags, advance PC by two, and add three nominal cycles.

#### Scenario: Borrow from the byte
- **WHEN** A=$00, the addressed byte is $01, and C=1
- **THEN** A=$FF, C=0, V=0, N=1, and Z=0

#### Scenario: Signed overflow and decimal flag
- **WHEN** A=$80, the addressed byte is $01, C=1, and D=1
- **THEN** A=$7F, C=1, V=1, N=0, Z=0, and D remains set

### Requirement: Preserve the zero-page read-modify-write bus sequence

Zero-page ASL, LSR, ROL, and ROR SHALL read the selected byte through Machine, write the original byte to the same
address, then write the resulting byte to that address. Each SHALL advance PC by two and add five nominal cycles.

#### Scenario: Write original before result
- **WHEN** one of the selected instructions modifies a zero-page byte
- **THEN** Machine receives the original-byte write followed by the modified-byte write, even when their values match

### Requirement: Execute ASL using zero-page addressing

Opcode $06 SHALL shift the addressed byte left, move its old bit 7 to C, insert zero into bit 0, and set N/Z from the
result. It SHALL preserve A and flags other than C/N/Z.

#### Scenario: Shift out the high bit
- **WHEN** the addressed byte is $80 and ASL executes
- **THEN** the addressed byte becomes $00, C=1, N=0, and Z=1

### Requirement: Execute LSR using zero-page addressing

Opcode $46 SHALL shift the addressed byte right, move its old bit 0 to C, insert zero into bit 7, and set N/Z from the
result. It SHALL preserve A and flags other than C/N/Z.

#### Scenario: Shift out the low bit
- **WHEN** the addressed byte is $01 and LSR executes
- **THEN** the addressed byte becomes $00, C=1, N=0, and Z=1

### Requirement: Execute ROL using zero-page addressing

Opcode $26 SHALL shift the addressed byte left, move its old bit 7 to C, insert the old C into bit 0, and set N/Z from
the result. It SHALL preserve A and flags other than C/N/Z.

#### Scenario: Rotate through a set carry
- **WHEN** the addressed byte is $80, C=1, and ROL executes
- **THEN** the addressed byte becomes $01, C=1, N=0, and Z=0

#### Scenario: Rotate with a clear carry
- **WHEN** the addressed byte is $40, C=0, and ROL executes
- **THEN** the addressed byte becomes $80, C=0, N=1, and Z=0

### Requirement: Execute ROR using zero-page addressing

Opcode $66 SHALL shift the addressed byte right, move its old bit 0 to C, insert the old C into bit 7, and set N/Z from
the result. It SHALL preserve A and flags other than C/N/Z.

#### Scenario: Rotate through a set carry
- **WHEN** the addressed byte is $01, C=1, and ROR executes
- **THEN** the addressed byte becomes $80, C=1, N=1, and Z=0

#### Scenario: Rotate with a clear carry
- **WHEN** the addressed byte is $02, C=0, and ROR executes
- **THEN** the addressed byte becomes $01, C=0, N=0, and Z=0

### Requirement: Execute AND using zero-page addressing

Opcode $25 SHALL read the zero-extended one-byte address through Machine, combine its byte with A using bitwise AND,
store the result in A, and set N/Z from that byte. It SHALL advance PC by two, add three nominal cycles, and preserve
other registers and flags.

#### Scenario: Produce zero
- **WHEN** A=$F0 and the addressed byte is $0F
- **THEN** A=$00, N=0, and Z=1

### Requirement: Execute ORA using zero-page addressing

Opcode $05 SHALL read the zero-extended one-byte address through Machine, combine its byte with A using bitwise OR,
store the result in A, and set N/Z from that byte. It SHALL advance PC by two, add three nominal cycles, and preserve
other registers and flags.

#### Scenario: Combine distinct bits
- **WHEN** A=$10 and the addressed byte is $80
- **THEN** A=$90, N=1, and Z=0

### Requirement: Execute EOR using zero-page addressing

Opcode $45 SHALL read the zero-extended one-byte address through Machine, combine its byte with A using bitwise
exclusive OR, store the result in A, and set N/Z from that byte. It SHALL advance PC by two, add three nominal cycles,
and preserve other registers and flags.

#### Scenario: Toggle matching bits
- **WHEN** A=$0F and the addressed byte is $8F
- **THEN** A=$80, N=1, and Z=0

### Requirement: Execute LDA using indexed-indirect addressing

Opcode $A1 SHALL add X to its one-byte operand modulo 256, read a little-endian pointer from that zero-page address
and the following zero-page address modulo 256, and read the target byte through Machine into A. It SHALL set N/Z
from that byte, advance PC by two, add six nominal cycles, and preserve other registers and flags.

#### Scenario: Wrap the indexed pointer address
- **WHEN** the operand is $F0, X=$20, $10/$11 contain $34/$12, and $1234 provides $80
- **THEN** A=$80, N=1, Z=0, and six cycles accrue

#### Scenario: Wrap the pointer's high-byte address
- **WHEN** the operand is $FC, X=$03, and $FF/$00 contain the low and high pointer bytes
- **THEN** the target byte is read through Machine using those bytes

### Requirement: Execute LDA using indirect-indexed addressing

Opcode $B1 SHALL read a little-endian pointer from the operand's zero-page address and the following zero-page address
modulo 256, add Y to it modulo 65536, and read the resulting address through Machine into A. It SHALL set N/Z from
that byte, advance PC by two, add five nominal cycles plus one on page crossing, and preserve other registers and flags.

#### Scenario: Wrap the pointer and cross a page
- **WHEN** the operand is $FF, $FF/$00 contain $FF/$12, Y=$01, and $1300 provides $00
- **THEN** A=$00, N=0, Z=1, and six cycles accrue

#### Scenario: Wrap the effective address
- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the byte at $0000 is loaded and six cycles accrue

#### Scenario: Index without crossing a page
- **WHEN** the pointer is $1230 and Y=$04
- **THEN** the byte at $1234 is loaded and five cycles accrue

### Requirement: Execute ADC with an immediate operand

Opcode $69 SHALL add A, the next byte, and the incoming C in binary, store the low eight bits in A, and set C from
unsigned carry, V from signed overflow, and N/Z from the result. It SHALL advance PC by two and add two nominal cycles,
preserving other registers and flags. D SHALL be preserved and SHALL NOT enable decimal arithmetic.

#### Scenario: Carry out of the byte
- **WHEN** A=$FF, the operand is $00, and C=1
- **THEN** A=$00, C=1, V=0, N=0, and Z=1

#### Scenario: Signed overflow
- **WHEN** A=$7F, the operand is $01, and C=0
- **THEN** A=$80, C=0, V=1, N=1, and Z=0

#### Scenario: Decimal flag does not change arithmetic
- **WHEN** A=$09, the operand is $01, C=0, and D=1
- **THEN** A=$0A and D remains set

### Requirement: Execute SBC with an immediate operand

Opcode $E9 SHALL subtract the next byte and the inverse of incoming C from A in binary, store the low eight bits in A,
and set C for no unsigned borrow, V from signed overflow, and N/Z from the result. It SHALL advance PC by two and add
two nominal cycles, preserving other registers and flags. D SHALL be preserved and SHALL NOT enable decimal arithmetic.

#### Scenario: Borrow from the byte
- **WHEN** A=$00, the operand is $01, and C=1
- **THEN** A=$FF, C=0, V=0, N=1, and Z=0

#### Scenario: Signed overflow
- **WHEN** A=$80, the operand is $01, and C=1
- **THEN** A=$7F, C=1, V=1, N=0, and Z=0

#### Scenario: Decimal flag does not change arithmetic
- **WHEN** A=$10, the operand is $01, C=1, and D=1
- **THEN** A=$0F and D remains set

### Requirement: Execute AND with an immediate operand

Opcode $29 SHALL combine A with the next byte using bitwise AND, store the result in A, and set N and Z from that
byte. It SHALL advance PC by two and add two nominal cycles, preserving other registers and flags.

#### Scenario: Produce zero
- **WHEN** A=$F0 and AND #$0F executes
- **THEN** A=$00, N=0, and Z=1

#### Scenario: Set the negative flag
- **WHEN** A=$FF and AND #$80 executes
- **THEN** A=$80, N=1, and Z=0

### Requirement: Execute ORA with an immediate operand

Opcode $09 SHALL combine A with the next byte using bitwise OR, store the result in A, and set N and Z from that
byte. It SHALL advance PC by two and add two nominal cycles, preserving other registers and flags.

#### Scenario: Produce zero
- **WHEN** A=$00 and ORA #$00 executes
- **THEN** A=$00, N=0, and Z=1

#### Scenario: Combine distinct bits
- **WHEN** A=$10 and ORA #$80 executes
- **THEN** A=$90, N=1, and Z=0

### Requirement: Execute EOR with an immediate operand

Opcode $49 SHALL combine A with the next byte using bitwise exclusive OR, store the result in A, and set N and Z from
that byte. It SHALL advance PC by two and add two nominal cycles, preserving other registers and flags.

#### Scenario: Produce zero
- **WHEN** A=$FF and EOR #$FF executes
- **THEN** A=$00, N=0, and Z=1

#### Scenario: Toggle matching bits
- **WHEN** A=$0F and EOR #$8F executes
- **THEN** A=$80, N=1, and Z=0

### Requirement: Execute STA using indexed-indirect addressing

Opcode $81 SHALL add X to its one-byte operand modulo 256, read the little-endian target pointer from that zero-page
address and the following zero-page address modulo 256, and write A through Machine to the target. It SHALL advance
PC by two, add six nominal cycles, and preserve other registers and flags.

#### Scenario: Wrap the indexed pointer address
- **WHEN** the operand is $F0, X=$20, and $10/$11 contain $34/$12
- **THEN** the write targets $1234 through Machine

#### Scenario: Wrap the pointer's high-byte address
- **WHEN** the operand is $FC, X=$03, and $FF/$00 contain $34/$12
- **THEN** the write targets $1234 through Machine

### Requirement: Execute STA using indirect-indexed addressing

Opcode $91 SHALL read a little-endian target pointer from the one-byte operand's zero-page address and the following
zero-page address modulo 256, add Y to the pointer modulo 65536, and write A through Machine to the result. It SHALL
advance PC by two, add six nominal cycles regardless of page crossing, and preserve other registers and flags.

#### Scenario: Wrap the pointer and cross a page
- **WHEN** the operand is $FF, $FF/$00 contain $FF/$12, and Y=$01
- **THEN** the write targets $1300 through Machine

#### Scenario: Wrap the effective address
- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the write targets $0000 through Machine

#### Scenario: Index without crossing a page
- **WHEN** the pointer is $1230 and Y=$04
- **THEN** the write targets $1234 through Machine and adds six nominal cycles

### Requirement: Execute ASL on the accumulator

Opcode $0A SHALL shift A left by one bit, set C from the old bit 7, insert zero into bit 0, and set N and Z from the
eight-bit result. It SHALL advance PC by one and add two nominal cycles, preserving the other registers and flags.

#### Scenario: Shift out the high bit
- **WHEN** A=$80 and ASL executes
- **THEN** A=$00, C=1, Z=1, and N=0

#### Scenario: Set the negative flag
- **WHEN** A=$40 and ASL executes
- **THEN** A=$80, C=0, Z=0, and N=1

### Requirement: Execute LSR on the accumulator

Opcode $4A SHALL shift A right by one bit, set C from the old bit 0, insert zero into bit 7, and set N and Z from the
eight-bit result. It SHALL advance PC by one and add two nominal cycles, preserving the other registers and flags.

#### Scenario: Shift out the low bit
- **WHEN** A=$01 and LSR executes
- **THEN** A=$00, C=1, Z=1, and N=0

#### Scenario: Shift the high bit
- **WHEN** A=$80 and LSR executes
- **THEN** A=$40, C=0, Z=0, and N=0

### Requirement: Execute ROL on the accumulator

Opcode $2A SHALL shift A left by one bit, set C from the old bit 7, insert the old C into bit 0, and set N and Z from
the eight-bit result. It SHALL advance PC by one and add two nominal cycles, preserving the other registers and flags.

#### Scenario: Rotate through a set carry
- **WHEN** A=$80, C=1, and ROL executes
- **THEN** A=$01, C=1, Z=0, and N=0

#### Scenario: Rotate with a clear carry
- **WHEN** A=$40, C=0, and ROL executes
- **THEN** A=$80, C=0, Z=0, and N=1

### Requirement: Execute ROR on the accumulator

Opcode $6A SHALL shift A right by one bit, set C from the old bit 0, insert the old C into bit 7, and set N and Z from
the eight-bit result. It SHALL advance PC by one and add two nominal cycles, preserving the other registers and flags.

#### Scenario: Rotate through a set carry
- **WHEN** A=$01, C=1, and ROR executes
- **THEN** A=$80, C=1, Z=0, and N=1

#### Scenario: Rotate with a clear carry
- **WHEN** A=$02, C=0, and ROR executes
- **THEN** A=$01, C=0, Z=0, and N=0

### Requirement: Execute CMP with an immediate operand

Opcode $C9 SHALL compare A with the next byte, set C if A is unsigned greater than or equal to the operand, set Z on
equality, and set N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add two nominal cycles,
preserving all registers other than PC and flags other than N/Z/C.

#### Scenario: Compare equal values
- **WHEN** A=$42 and CMP #$42 executes
- **THEN** C=1, Z=1, and N=0

#### Scenario: Compare unequal values
- **WHEN** A=$00 with operand $01, or A=$80 with operand $01, is compared
- **THEN** N/Z/C are respectively 1/0/0 and 0/0/1

### Requirement: Execute CPX with an immediate operand

Opcode $E0 SHALL compare X with the next byte, set C if X is unsigned greater than or equal to the operand, set Z on
equality, and set N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add two nominal cycles,
preserving all registers other than PC and flags other than N/Z/C.

#### Scenario: Compare equal values
- **WHEN** X=$42 and CPX #$42 executes
- **THEN** C=1, Z=1, and N=0

#### Scenario: Compare unequal values
- **WHEN** X=$00 with operand $01, or X=$80 with operand $01, is compared
- **THEN** N/Z/C are respectively 1/0/0 and 0/0/1

### Requirement: Execute CPY with an immediate operand

Opcode $C0 SHALL compare Y with the next byte, set C if Y is unsigned greater than or equal to the operand, set Z on
equality, and set N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add two nominal cycles,
preserving all registers other than PC and flags other than N/Z/C.

#### Scenario: Compare equal values
- **WHEN** Y=$42 and CPY #$42 executes
- **THEN** C=1, Z=1, and N=0

#### Scenario: Compare unequal values
- **WHEN** Y=$00 with operand $01, or Y=$80 with operand $01, is compared
- **THEN** N/Z/C are respectively 1/0/0 and 0/0/1

### Requirement: Execute JMP using absolute addressing

Opcode $4C SHALL load PC from its little-endian two-byte operand and add three cycles. All other registers, flags, and
memory SHALL remain unchanged.

#### Scenario: Jump to an asymmetric address
- **WHEN** $4C $34 $12 executes at $0000
- **THEN** PC becomes $1234, cycles increase by three

#### Scenario: Wrap an operand fetch
- **WHEN** opcode and operand bytes straddle $FFFF and $0000 in synthetic connected memory
- **THEN** operand fetch wraps at 16 bits and PC becomes the decoded target

### Requirement: Execute JMP using indirect addressing

Opcode $6C SHALL read a little-endian pointer from its operand and load PC from the two pointed-to bytes. The
high-byte read SHALL wrap within the pointer page. It SHALL add five cycles, preserve all other CPU registers and
flags, and perform no memory writes.

#### Scenario: Resolve a pointer
- **WHEN** JMP ($1234) reads $78 at $1234 and $56 at $1235 through connected memory
- **THEN** PC becomes $5678, five cycles accrue

#### Scenario: Emulate page-boundary behavior
- **WHEN** JMP ($12FF) reads $78 at $12FF and $56 at $1200
- **THEN** PC becomes $5678 and the high byte is not read from $1300

### Requirement: Execute JSR using absolute addressing

Opcode $20 SHALL call the little-endian absolute target, pushing the address of its last operand byte high byte first
to $0100+SP, decrementing SP modulo 256 after each write. It SHALL add six cycles and preserve A/X/Y and all flags.

#### Scenario: Push the return address and call
- **WHEN** JSR $1234 at $8000 executes with SP=$FD
- **THEN** $80 is written to $01FD, $02 to $01FC, SP becomes $FB, PC becomes $1234, and six cycles accrue

#### Scenario: Wrap the stack pointer
- **WHEN** JSR executes with SP=$00
- **THEN** its high and low return bytes are written to $0100 and $01FF in that order and SP becomes $FE

#### Scenario: Fetch the high operand after stack writes
- **WHEN** the high operand aliases a stack destination in connected RAM
- **THEN** the high target byte is read after both writes

### Requirement: Execute RTS using implied addressing

Opcode $60 SHALL increment SP and read the low return byte at $0100+SP, then increment SP and read its high byte. It
SHALL set PC to that word plus one modulo 65536, add six cycles, and preserve A/X/Y, flags, and memory.

#### Scenario: Return using stack bytes
- **WHEN** RTS executes with SP=$FB, $02 at $01FC, and $80 at $01FD
- **THEN** SP becomes $FD, PC becomes $8003, and six cycles accrue

#### Scenario: Wrap stack and return address
- **WHEN** SP=$FE and $FF is stored at both $01FF and $0100
- **THEN** RTS reads low then high through connected memory, leaves SP=$00, and sets PC=$0000

### Requirement: Execute STA using zero page addressing

Opcode $85 SHALL use the zero-extended one-byte operand to write A to memory and preserve all flags. It SHALL advance
PC by two bytes modulo 65536, add three cycles, and preserve all registers other than PC.

#### Scenario: Access the selected address
- **WHEN** STA zero page ($85) executes and the operand is $FF
- **THEN** it writes to $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

### Requirement: Execute STX using zero page addressing

Opcode $86 SHALL use the zero-extended one-byte operand to write X to memory and preserve all flags. It SHALL advance
PC by two bytes modulo 65536, add three cycles, and preserve all registers other than PC.

#### Scenario: Access the selected address
- **WHEN** STX zero page ($86) executes and the operand is $FF
- **THEN** it writes to $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

### Requirement: Execute STY using zero page addressing

Opcode $84 SHALL use the zero-extended one-byte operand to write Y to memory and preserve all flags. It SHALL advance
PC by two bytes modulo 65536, add three cycles, and preserve all registers other than PC.

#### Scenario: Access the selected address
- **WHEN** STY zero page ($84) executes and the operand is $FF
- **THEN** it writes to $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

### Requirement: Execute LDA using zero page addressing

Opcode $A5 SHALL use the zero-extended one-byte operand to read the byte into A, set N from bit 7, and set Z exactly
when the byte is zero. It SHALL advance PC by two bytes modulo 65536, add three cycles, and preserve all registers
other than A and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDA zero page ($A5) executes and the operand is $FF
- **THEN** it reads from $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** A holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDX using zero page addressing

Opcode $A6 SHALL use the zero-extended one-byte operand to read the byte into X, set N from bit 7, and set Z exactly
when the byte is zero. It SHALL advance PC by two bytes modulo 65536, add three cycles, and preserve all registers
other than X and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDX zero page ($A6) executes and the operand is $FF
- **THEN** it reads from $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** X holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDY using zero page addressing

Opcode $A4 SHALL use the zero-extended one-byte operand to read the byte into Y, set N from bit 7, and set Z exactly
when the byte is zero. It SHALL advance PC by two bytes modulo 65536, add three cycles, and preserve all registers
other than Y and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDY zero page ($A4) executes and the operand is $FF
- **THEN** it reads from $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** Y holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute STA using absolute,X addressing

Opcode $9D SHALL use the little-endian operand plus X modulo 65536 to write A to memory and preserve all flags. It
SHALL advance PC by three bytes modulo 65536, add five cycles regardless of page crossing, and preserve all registers
other than PC.

#### Scenario: Access the selected address
- **WHEN** STA absolute,X ($9D) executes and the operand is $00FF and X=$01
- **THEN** it writes to $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and X=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five cycles in both cases

### Requirement: Execute STA using absolute,Y addressing

Opcode $99 SHALL use the little-endian operand plus Y modulo 65536 to write A to memory and preserve all flags. It
SHALL advance PC by three bytes modulo 65536, add five cycles regardless of page crossing, and preserve all registers
other than PC.

#### Scenario: Access the selected address
- **WHEN** STA absolute,Y ($99) executes and the operand is $00FF and Y=$01
- **THEN** it writes to $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and Y=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five cycles in both cases

### Requirement: Execute LDA using absolute,X addressing

Opcode $BD SHALL use the little-endian operand plus X modulo 65536 to read the byte into A, set N from bit 7, and set
Z exactly when the byte is zero. It SHALL advance PC by three bytes modulo 65536, add four cycles plus one on a page
crossing, and preserve all registers other than A and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDA absolute,X ($BD) executes and the operand is $00FF and X=$01
- **THEN** it reads from $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and X=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five and four cycles respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** A holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDA using absolute,Y addressing

Opcode $B9 SHALL use the little-endian operand plus Y modulo 65536 to read the byte into A, set N from bit 7, and set
Z exactly when the byte is zero. It SHALL advance PC by three bytes modulo 65536, add four cycles plus one on a page
crossing, and preserve all registers other than A and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDA absolute,Y ($B9) executes and the operand is $00FF and Y=$01
- **THEN** it reads from $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and Y=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five and four cycles respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** A holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDX using absolute,Y addressing

Opcode $BE SHALL use the little-endian operand plus Y modulo 65536 to read the byte into X, set N from bit 7, and set
Z exactly when the byte is zero. It SHALL advance PC by three bytes modulo 65536, add four cycles plus one on a page
crossing, and preserve all registers other than X and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDX absolute,Y ($BE) executes and the operand is $00FF and Y=$01
- **THEN** it reads from $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and Y=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five and four cycles respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** X holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDY using absolute,X addressing

Opcode $BC SHALL use the little-endian operand plus X modulo 65536 to read the byte into Y, set N from bit 7, and set
Z exactly when the byte is zero. It SHALL advance PC by three bytes modulo 65536, add four cycles plus one on a page
crossing, and preserve all registers other than Y and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDY absolute,X ($BC) executes and the operand is $00FF and X=$01
- **THEN** it reads from $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and X=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five and four cycles respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** Y holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute INC using absolute addressing

Opcode $EE SHALL decode a little-endian 16-bit operand and use it directly as the destination. Through Machine it SHALL
read the byte, write the original byte, and write (original + 1) modulo 256 to that address. It SHALL set N/Z from the
result, advance PC by three and add six nominal cycles.

#### Scenario: Decode the address in little-endian order

- **WHEN** operand bytes are $34 followed by $02
- **THEN** the destination is $0234, PC advances by three, and six cycles accrue

#### Scenario: Write the old byte and then the wrapped result

- **WHEN** the destination initially contains $FF
- **THEN** the instruction reads it, writes $FF then $00 to that address, and sets N=0 and Z=1

#### Scenario: Set flags from the resulting byte

- **WHEN** the destination initially contains $7F
- **THEN** it ends at $80 with N=1 and Z=0

### Requirement: Execute DEC using absolute addressing

Opcode $CE SHALL decode a little-endian 16-bit operand and use it directly as the destination. Through Machine it SHALL
read the byte, write the original byte, and write (original - 1) modulo 256 to that address. It SHALL set N/Z from the
result, advance PC by three and add six nominal cycles.

#### Scenario: Decode the address in little-endian order

- **WHEN** operand bytes are $34 followed by $02
- **THEN** the destination is $0234, PC advances by three, and six cycles accrue

#### Scenario: Write the old byte and then the wrapped result

- **WHEN** the destination initially contains $00
- **THEN** the instruction reads it, writes $00 then $FF to that address, and sets N=1 and Z=0

#### Scenario: Set flags from the resulting byte

- **WHEN** the destination initially contains $01
- **THEN** it ends at $00 with N=0 and Z=1

### Requirement: Execute INC using absolute,X addressing

Opcode $FE SHALL decode a little-endian 16-bit operand and use that address plus X modulo 65536 as the destination.
Through Machine it SHALL read the byte, write the original byte, and write (original + 1) modulo 256 to that address. It
SHALL set N/Z from the result, advance PC by three and add seven fixed nominal cycles.

#### Scenario: Index with and without a page crossing

- **WHEN** base=$02FC and X=$01 or $04
- **THEN** the destination is $02FD or $0300; both cost seven cycles and consume three instruction bytes

#### Scenario: Wrap the indexed destination

- **WHEN** base=$FFFF and X=$01
- **THEN** the read and writes access $0000 and the instruction still costs seven cycles

#### Scenario: Write the old byte and then the wrapped result

- **WHEN** the destination initially contains $FF
- **THEN** the instruction reads it, writes $FF then $00 to that address, and sets N=0 and Z=1

#### Scenario: Set flags from the resulting byte

- **WHEN** the destination initially contains $7F
- **THEN** it ends at $80 with N=1 and Z=0

### Requirement: Execute DEC using absolute,X addressing

Opcode $DE SHALL decode a little-endian 16-bit operand and use that address plus X modulo 65536 as the destination.
Through Machine it SHALL read the byte, write the original byte, and write (original - 1) modulo 256 to that address. It
SHALL set N/Z from the result, advance PC by three and add seven fixed nominal cycles.

#### Scenario: Index with and without a page crossing

- **WHEN** base=$02FC and X=$01 or $04
- **THEN** the destination is $02FD or $0300; both cost seven cycles and consume three instruction bytes

#### Scenario: Wrap the indexed destination

- **WHEN** base=$FFFF and X=$01
- **THEN** the read and writes access $0000 and the instruction still costs seven cycles

#### Scenario: Write the old byte and then the wrapped result

- **WHEN** the destination initially contains $00
- **THEN** the instruction reads it, writes $00 then $FF to that address, and sets N=1 and Z=0

#### Scenario: Set flags from the resulting byte

- **WHEN** the destination initially contains $01
- **THEN** it ends at $00 with N=0 and Z=1

### Requirement: Execute ORA using indexed-indirect addressing

Opcode $01 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL store A OR operand in A and set N/Z from the result.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $35/$CA or $00/$00
- **THEN** A becomes $FF with N=1, Z=0 or $00 with N=0, Z=1, respectively

### Requirement: Execute AND using indexed-indirect addressing

Opcode $21 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL store A AND operand in A and set N/Z from the result.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $F0/$0F or $FF/$80
- **THEN** A becomes $00 with N=0, Z=1 or $80 with N=1, Z=0, respectively

### Requirement: Execute EOR using indexed-indirect addressing

Opcode $41 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL store A XOR operand in A and set N/Z from the result.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $FF/$FF or $7F/$FF
- **THEN** A becomes $00 with N=0, Z=1 or $80 with N=1, Z=0, respectively

### Requirement: Execute AND using indirect-indexed addressing

Opcode $31 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL store A AND operand in A and set N/Z from the result.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $F0/$0F or $FF/$80
- **THEN** A becomes $00 with N=0, Z=1 or $80 with N=1, Z=0, respectively

### Requirement: Execute ORA using indirect-indexed addressing

Opcode $11 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL store A OR operand in A and set N/Z from the result.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $35/$CA or $00/$00
- **THEN** A becomes $FF with N=1, Z=0 or $00 with N=0, Z=1, respectively

### Requirement: Execute EOR using indirect-indexed addressing

Opcode $51 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL store A XOR operand in A and set N/Z from the result.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $FF/$FF or $7F/$FF
- **THEN** A becomes $00 with N=0, Z=1 or $80 with N=1, Z=0, respectively

### Requirement: Execute ADC using indexed-indirect addressing

Opcode $61 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL add A, the operand and incoming C in binary regardless of D, store the low byte in A,
and set N/Z from A, C for carry out, and V for signed overflow.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** D is clear or set and A/operand/C are $7F/$00/1, $FF/$00/1, or $01/$01/0
- **THEN** A/C/V/N/Z become $80/0/1/1/0, $00/1/0/0/1, or $02/0/0/0/0, respectively, with no decimal correction

### Requirement: Execute ADC using indirect-indexed addressing

Opcode $71 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL add A, the operand and incoming C in binary regardless of D, store the low byte in
A, and set N/Z from A, C for carry out, and V for signed overflow.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** D is clear or set and A/operand/C are $7F/$00/1, $FF/$00/1, or $01/$01/0
- **THEN** A/C/V/N/Z become $80/0/1/1/0, $00/1/0/0/1, or $02/0/0/0/0, respectively, with no decimal correction

### Requirement: Execute SBC using indexed-indirect addressing

Opcode $E1 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL subtract the operand and (1 - C) from A in binary regardless of D, store the low byte
in A, and set N/Z from A, C for no unsigned borrow, and V for signed overflow.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** D is clear or set and A/operand/C are $80/$01/1, $00/$00/0, or $42/$42/1
- **THEN** A/C/V/N/Z become $7F/1/1/0/0, $FF/0/0/1/0, or $00/1/0/0/1, respectively, with no decimal correction

### Requirement: Execute SBC using indirect-indexed addressing

Opcode $F1 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL subtract the operand and (1 - C) from A in binary regardless of D, store the low
byte in A, and set N/Z from A, C for no unsigned borrow, and V for signed overflow.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** D is clear or set and A/operand/C are $80/$01/1, $00/$00/0, or $42/$42/1
- **THEN** A/C/V/N/Z become $7F/1/1/0/0, $FF/0/0/1/0, or $00/1/0/0/1, respectively, with no decimal correction

### Requirement: Execute CMP using indexed-indirect addressing

Opcode $C1 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL leave A intact and set C if A is at least the operand unsigned, Z if equal, and N from
bit 7 of the wrapped difference.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** A=$40 and the addressed byte is $41, $40, or $3F
- **THEN** C/Z/N are 0/0/1, 1/1/0, or 1/0/0 respectively and A remains $40.

### Requirement: Execute CMP using indirect-indexed addressing

Opcode $D1 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL leave A intact and set C if A is at least the operand unsigned, Z if equal, and N
from bit 7 of the wrapped difference.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** A=$40 and the addressed byte is $41, $40, or $3F
- **THEN** C/Z/N are 0/0/1, 1/1/0, or 1/0/0 respectively and A remains $40.

### Requirement: Execute PHA using implied addressing

Opcode $48 SHALL write A through Machine at $0100 | SP and then decrement SP modulo 256. It SHALL leave the status flags
unchanged, advance PC by one, and add three cycles.

#### Scenario: Save the accumulator at the pre-decrement position

- **WHEN** A=$80 and SP=$FD
- **THEN** $01FD receives $80, SP=$FC, PC advances by one, and three cycles accrue

#### Scenario: Wrap after pushing to the bottom of the stack page

- **WHEN** A=$00 and SP=$00
- **THEN** $0100 receives $00 and SP becomes $FF

### Requirement: Execute PLA using implied addressing

Opcode $68 SHALL increment SP modulo 256, load A from $0100 | SP through Machine, and set N/Z from A. It SHALL advance
PC by one and add four cycles.

#### Scenario: Load a negative value

- **WHEN** SP=$FC and $01FD holds $80
- **THEN** A=$80, N=1, Z=0, SP=$FD, PC advances by one, and four cycles accrue

#### Scenario: Pull zero using a wrapped stack pointer

- **WHEN** SP=$FF and $0100 holds $00
- **THEN** A=$00, N=0, Z=1, and SP becomes $00

### Requirement: Execute PHP using implied addressing

Opcode $08 SHALL write the status byte with bits 5 and 4 set through Machine at $0100 | SP, then decrement SP modulo
256. It SHALL leave the status fields unchanged, advance PC by one, and add three cycles.

#### Scenario: Force B in the saved byte without setting it in the CPU

- **WHEN** PHP executes with P=$A5 and SP=$FD
- **THEN** $01FD receives $B5, P stays $A5, SP=$FC, PC advances by one, and three cycles accrue

#### Scenario: Wrap the stack pointer after pushing

- **WHEN** SP=$00 and P=$7B
- **THEN** $0100 receives $7B and SP becomes $FF

### Requirement: Execute PLP using implied addressing

Opcode $28 SHALL increment SP modulo 256 and read the byte at $0100 | SP through Machine. It SHALL restore N/V/D/I/Z/C
from that byte, ignore bits 5 and 4, and preserve `break_flag`. It SHALL advance PC by one and add four cycles.

#### Scenario: Restore hardware flags on a wrapping pull

- **WHEN** PLP executes with SP=$FF, software B=1, and $CB at $0100
- **THEN** SP=$00, displayed P=$FB, PC advances by one, and four cycles accrue

#### Scenario: Ignore set B and bit 5 in the stack byte

- **WHEN** software B=0 and the pulled byte is $30
- **THEN** all six hardware flags are cleared and displayed P=$20

### Requirement: Execute BRK using implied addressing

Opcode $00 SHALL push the high byte then the low byte of the opcode address plus two, then the pre-instruction status
with bits 5 and 4 set. Each push writes through Machine at $0100 | SP and then decrements SP modulo 256. BRK SHALL set
I, read vector bytes $FFFE then $FFFF through Machine into PC in little-endian order, and add seven cycles. It SHALL
execute even when I is already set and leave the software B field unchanged.

#### Scenario: Save the resume address and old status

- **WHEN** BRK executes at $0234 with SP=$FD, I=0, P=$29, and $34/$C2 in the vector
- **THEN** $01FD/$01FC/$01FB receive $02/$36/$39, SP=$FA, I=1, PC=$C234, and seven cycles accrue

#### Scenario: Wrap the stack with interrupts masked

- **WHEN** BRK executes with SP=$00, I=1, and a known vector
- **THEN** the frame occupies $0100/$01FF/$01FE in push order, SP=$FD, and PC loads the vector

### Requirement: Execute RTI using implied addressing

Opcode $40 SHALL pull status, PC low, then PC high. Each pull increments SP modulo 256 before reading $0100 | SP through
Machine. RTI SHALL restore N/V/D/I/Z/C, ignore stack status bits 5 and 4 and preserve `break_flag`. It SHALL load PC
from the two address bytes without adjustment and add six cycles.

#### Scenario: Resume exactly at the stacked address

- **WHEN** SP=$FA, software B=0, and $BA/$34/$C2 are at $01FB-$01FD
- **THEN** SP=$FD, displayed P=$AA, PC=$C234, and six cycles accrue

#### Scenario: Pull across the end of the stack page

- **WHEN** SP=$FE, software B=1, and $01/$78/$56 are at $01FF/$0100/$0101
- **THEN** SP=$01, displayed P=$31, and PC=$5678
