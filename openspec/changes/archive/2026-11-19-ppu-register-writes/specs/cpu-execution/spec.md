## MODIFIED Requirements

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
