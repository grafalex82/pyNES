# Spec Delta

## Purpose

Establish observable CPU register state and perform functional startup and repeated reset through connected memory,
without fetching instructions or modeling physical reset timing. Register inputs are assumed to be integers;
boolean flag inputs are assumed valid.

## ADDED Requirements

### Requirement: Expose CPU register state

The CPU state interface SHALL expose read/write properties `a`, `x`, `y`, `sp`, `pc`, and processor status `p`.
A, X, Y, and SP SHALL represent byte registers and PC SHALL represent a 16-bit address.
Register state SHALL be independent between CPUs.

#### Scenario: Set a known pre-reset state

- **WHEN** a caller assigns valid nonzero register values to one initialized CPU
- **THEN** the corresponding values can be inspected without accessing private fields
- **AND** another CPU's state remains unchanged

### Requirement: Assert register value ranges

The A/X/Y/SP/P setters SHALL use ordinary Python assertions for 0..255 and PC for 0..65535 before changing state.
With assertions enabled, out-of-range assignments SHALL raise AssertionError and leave state unchanged.
Values SHALL NOT be truncated. These checks SHALL follow standard Python assertion behavior, including omission
under optimized execution.

#### Scenario: Accept range endpoints

- **WHEN** a caller assigns zero or the maximum value to a register
- **THEN** the assignment succeeds
- **AND** reading the register returns that value, with P's normal bit 5 normalization

#### Scenario: Reject values outside the range

- **WHEN** assertions are enabled and a caller assigns -1 or one above a register's maximum
- **THEN** AssertionError is raised before any register or status field changes

### Requirement: Store flags separately and convert the status byte

Flags SHALL be separate booleans exposed as read/write properties `negative` (N), `overflow` (V), `break_flag` (B),
`decimal` (D), `interrupt_disable` (I), `zero` (Z), and `carry` (C). Reading `p` SHALL pack NV1BDIZC;
assigning `p` SHALL replace all seven flags. B SHALL be a software field in bit 4.
Bit 5 SHALL read as 1 and be ignored on assignment, with no stored variable. No packed P SHALL be stored.

#### Scenario: Edit an individual flag through its property

- **WHEN** a caller assigns a boolean to one flag property
- **THEN** reading `p` immediately reflects the new value in that flag's bit
- **AND** the other flag properties remain unchanged

#### Scenario: Normalize a displayed status value

- **WHEN** P is assigned a byte with selected flag values and either value in bit 5
- **THEN** reading P preserves all seven assigned flag values, including B in bit 4, and reports bit 5 as 1

#### Scenario: Pack and unpack the B flag

- **WHEN** `p` is assigned $10
- **THEN** `break_flag` is true, the six hardware flags are false, and reading `p` returns $30
- **WHEN** `break_flag` is then assigned false
- **THEN** reading `p` returns $20

#### Scenario: Replace previously set flag values

- **WHEN** `p` is assigned $FF
- **THEN** all seven flags are true and reading `p` returns $FF
- **WHEN** `p` is then assigned $00
- **THEN** each flag property becomes false and reading `p` returns $20 rather than retaining earlier flag values
- **AND** a subsequent reset sets only I among those flags, so reading `p` returns $24

### Requirement: Establish initial CPU state

Constructing a CPU against connected memory SHALL produce A=X=Y=$00, SP=$FD, and flags I=1 with N,V,B,D,Z,C=0.
Displayed P SHALL be $24, and PC SHALL be obtained from the reset vector. CPU construction SHALL NOT clear memory.

#### Scenario: Initialize a CPU after memory is connected

- **WHEN** a CPU is constructed against a supported memory configuration containing a known reset vector
- **THEN** its final register state matches this initial profile and PC equals the vector's decoded address
- **AND** memory bytes written before CPU construction remain unchanged

### Requirement: Load the reset vector through the connected byte interface

Startup and each repeated reset SHALL read the low byte at $FFFC followed by the high byte at $FFFD through the
connected memory interface and set PC to their little-endian address. This functional operation SHALL perform no
opcode fetch, memory write, target-address validation, or peripheral access.

#### Scenario: Decode an asymmetric vector

- **WHEN** the vector bytes are $34 at $FFFC and $12 at $FFFD
- **THEN** PC becomes $1234 after those two ordered reads rather than $3412 or $FFFC

#### Scenario: Reload a vector without fetching its target

- **WHEN** a later reset observes different vector bytes that point to an unimplemented device address
- **THEN** PC takes the new vector value and no read is made at that target address

### Requirement: Apply NES repeated-reset register effects

A repeated reset SHALL decrement SP by 3 modulo 256, set I, preserve A/X/Y and N/V/B/D/Z/C, and reload PC
from the reset vector.
It SHALL leave every memory byte unchanged, including the stack page, and SHALL NOT rerun initial register clearing.
B preservation SHALL be a software-model convention rather than a physical reset effect.

#### Scenario: Preserve established state on reset

- **WHEN** reset is requested after A/X/Y, real flags, SP, and RAM contain known non-default values
- **THEN** only PC, SP, and I change according to reset behavior and memory is unchanged
- **AND** D is preserved even though NES decimal arithmetic is disabled

#### Scenario: Preserve the software B field on repeated reset

- **WHEN** `p` is assigned $10 and a repeated reset completes
- **THEN** `break_flag` remains true, I is set, and reading `p` returns $34
- **AND** SP and PC follow the specified reset behavior

#### Scenario: Wrap the stack pointer

- **WHEN** SP is $01 before a repeated reset
- **THEN** SP becomes $FE and no stack bytes are written

### Requirement: Make completed resets observable in debug logging

When CPU debug logging is enabled, each completed startup/reset SHALL emit a reset event containing the resulting
A, X, Y, SP, PC, and displayed P. This event SHALL describe completion without claiming an instruction was executed.

#### Scenario: Observe reset completion

- **WHEN** a reset completes with CPU debug logging enabled
- **THEN** one reset event reports its resulting register values
- **AND** the event identifies reset completion rather than an executed instruction
