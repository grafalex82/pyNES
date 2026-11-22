# CPU NMI Entry

## ADDED Requirements

### Requirement: Enter a pending NMI at an instruction boundary

NMI entry SHALL push the current PC high byte, low byte, and pre-entry status via Machine using stack-page
wrapping. The saved status SHALL have bit 5 set and bit 4 clear. Entry SHALL set I, read $FFFA then $FFFB into
PC in little-endian order, and add seven nominal cycles. Entry SHALL work regardless of I and preserve software B.

#### Scenario: Resume from a non-maskable interrupt

- **WHEN** NMI is serviced with I already set and the next instruction at a known PC
- **THEN** the stack contains the exact resume address and the pre-entry flags with the required status bits
- **AND** the handler address is loaded without executing its first instruction as part of entry
- **AND** RTI resumes at the saved PC
