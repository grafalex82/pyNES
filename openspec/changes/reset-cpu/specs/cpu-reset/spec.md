# Spec Delta

## Purpose

Establish observable CPU register state and perform functional startup and repeated reset through connected memory,
without fetching instructions or modeling physical reset timing. Caller-supplied register values are assumed valid.

## ADDED Requirements

### Requirement: Expose CPU register state

The CPU state interface SHALL allow reading and setting A, X, Y, SP, PC, and processor status P. A, X, Y, and SP SHALL
represent byte registers and PC SHALL represent a 16-bit address. Register state SHALL be independent between CPUs.

#### Scenario: Set a known pre-reset state

- **WHEN** a caller assigns valid nonzero register values to one initialized CPU
- **THEN** the corresponding values can be inspected without accessing private fields
- **AND** another CPU's state remains unchanged

### Requirement: Store flags separately and convert the status byte

N, V, D, I, Z, and C SHALL each be stored as a separate boolean variable. get_p() SHALL assemble a byte from their
current values; set_p() SHALL decode a byte into all six variables. No packed P byte SHALL be retained as state.
Flag positions SHALL follow the processor documentation. get_p() SHALL report bit 5 as 1 and bit 4 as 0; set_p()
SHALL ignore those two bits, which SHALL NOT have stored variables.

#### Scenario: Normalize a displayed status value

- **WHEN** P is assigned a byte with selected real flags and either value in bits 5 and 4
- **THEN** reading P preserves the six assigned flag values and reports bit 5 as 1 and bit 4 as 0

#### Scenario: Replace previously set flag values

- **WHEN** set_p() receives a byte with all six real flags set and then a byte with all six flags clear
- **THEN** each flag variable becomes false and get_p() returns $20 rather than retaining earlier flag values
- **AND** a subsequent reset sets only I among those flags, so get_p() returns $24

### Requirement: Establish initial CPU state

Constructing a CPU against connected memory SHALL produce A=X=Y=$00, SP=$FD, and meaningful flags I=1 with N,V,D,Z,C=0.
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

A repeated reset SHALL decrement SP by 3 modulo 256, set I, preserve A/X/Y and N/V/D/Z/C, and reload PC from the vector.
It SHALL leave every memory byte unchanged, including the stack page, and SHALL NOT rerun initial register clearing.

#### Scenario: Preserve established state on reset

- **WHEN** reset is requested after A/X/Y, real flags, SP, and RAM contain known non-default values
- **THEN** only PC, SP, and I change according to reset behavior and memory is unchanged
- **AND** D is preserved even though NES decimal arithmetic is disabled

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
