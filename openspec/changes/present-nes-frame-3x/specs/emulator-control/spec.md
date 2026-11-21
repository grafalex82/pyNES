# Video Progress and Frame Output

## ADDED Requirements

### Requirement: Advance PPU timing with nominal CPU cycles

The facade SHALL advance the PPU with cycles consumed by each completed execution step. The PPU SHALL
set vblank once per approximate frame and clear it by the start of the next visible period. Repeated status
reads SHALL leave the timing phase unchanged. A zero cycle budget SHALL leave video timing unchanged.

#### Scenario: Observe frame progress independently of polling

- **WHEN** execution crosses consecutive vblank boundaries with or without intervening status reads
- **THEN** each vblank flag becomes observable at its scheduled boundary
- **AND** reading status early in a frame does not cause an early vblank

### Requirement: Service PPU NMI through the execution facade

The facade SHALL service a pending PPU NMI at the resulting instruction boundary. It SHALL preserve one
executed instruction per step, include the NMI entry cycles in the elapsed budget, and advance the PPU by
those cycles. The next step SHALL start with the handler instruction.

#### Scenario: Interrupt a synthetic frame wait

- **WHEN** a synthetic program waits for a RAM byte incremented by its enabled NMI handler
- **THEN** the facade enters the handler once for the vblank edge and the handler updates the byte and returns
- **AND** the waiting program resumes without an extra opcode fetch during entry

### Requirement: Make completed frames available to the host

When frame output is enabled, each vblank entry SHALL publish one native-size frame composed from the PPU
state at that boundary. The host SHALL be able to present the most recent completed frame.

#### Scenario: Publish before the interrupt updates video memory

- **WHEN** a program writes a color during its vblank NMI handler
- **THEN** the captured frame at the interrupt boundary has the previous color
- **AND** the next completed frame can present the updated color
