# emulator-control Specification

## Purpose

Provide the host UI with one execution-control boundary for a connected emulator instance, supporting individual
instructions, execution bounded by CPU cycles, and a shared reset request without placing UI logic in devices.
Cycle budgets are assumed to be nonnegative integers. Breakpoint registration and callbacks remain future behavior.

## Requirements

### Requirement: Initialize one connected emulator instance

The execution facade SHALL initialize one CPU against the supplied connected Machine without executing an instruction.
It SHALL preserve that Machine and its memory. Separate facade instances SHALL have independent CPU state when
constructed with separate memory configurations.

#### Scenario: Prepare an instance without executing the entry instruction

- **WHEN** a facade is created for a supported connected cartridge whose entry byte is SEI
- **THEN** CPU startup loads the reset-vector address and establishes its existing initial register profile
- **AND** no entry instruction executes and preexisting RAM remains unchanged

### Requirement: Execute one instruction through the facade

The UI-facing step operation SHALL execute exactly one CPU instruction in the current instance.
It SHALL preserve CPU execution semantics and propagate failures without hiding or retrying them.

#### Scenario: Return after one SEI

- **WHEN** the current instruction is SEI followed by an unsupported opcode and the UI requests one step
- **THEN** SEI completes, control returns to the caller, and PC identifies the untouched next instruction

### Requirement: Execute a block with a CPU cycle budget

The UI-facing block operation SHALL accept a CPU cycle budget and execute sequential single steps until the increase
in CPU.cycles since call entry reaches that budget, or an exception occurs. A zero budget SHALL execute nothing.
Each call SHALL measure a new budget from the actual entry counter, without resetting CPU state.
The budget SHALL use actual instruction costs rather than an instruction count.

#### Scenario: Reach an exact cycle budget

- **WHEN** a caller with I clear requests six cycles from SEC, CLC, NOP, SEI
- **THEN** three instructions complete, PC advances by three, CPU.cycles increases by six, and C is clear
- **AND** control returns before SEI, so I remains clear

#### Scenario: Measure elapsed cycles from a nonzero entry counter

- **WHEN** CPU.cycles is already 10 after prior execution and a caller requests four cycles of NOPs
- **THEN** two NOPs execute and CPU.cycles becomes 14, rather than treating four as an absolute counter target

#### Scenario: Request an empty cycle budget

- **WHEN** a caller requests zero cycles
- **THEN** registers, flags, cycles, and memory remain unchanged and no instruction is fetched or traced

#### Scenario: Return before an unsupported instruction at the boundary

- **WHEN** SEI is followed by an unsupported opcode and the caller requests two cycles
- **THEN** SEI completes and the block returns before fetching the unsupported opcode

#### Scenario: Encounter missing behavior before the budget is reached

- **WHEN** SEI is followed by an unsupported opcode and the caller requests three cycles
- **THEN** SEI completes and the next step's exception propagates immediately with two cycles of progress retained
- **AND** the failed instruction is not skipped, no extra cycles are charged, and no further instruction is attempted

### Requirement: Finish the instruction that reaches the cycle budget

A block SHALL execute whole instructions and stop at the first instruction boundary where its cycle budget is met.
The last instruction SHALL complete even if its cost makes elapsed cycles exceed the budget; no instruction SHALL
be split or followed by an extra step after that boundary. Overshoot SHALL remain in CPU.cycles and SHALL NOT be
deducted from a later call's newly requested budget.

#### Scenario: Exceed an odd budget with two-cycle instructions

- **WHEN** a caller requests three cycles of NOPs
- **THEN** two complete NOPs execute and CPU.cycles increases by four
- **AND** no third NOP is fetched

#### Scenario: Start the next budget from the actual counter

- **WHEN** a caller requests three cycles twice in a row from two-cycle instructions
- **THEN** each call consumes four cycles and the combined increase is eight
- **AND** CPU state is not reset between calls

### Requirement: Coordinate reset through the facade

The UI-facing reset operation SHALL apply the existing repeated CPU reset to the current instance.
It SHALL preserve Machine, RAM, and cycles, reload PC, decrement SP by three modulo 256, and set I
while preserving the CPU's other existing reset state. It SHALL execute no instruction or constructor-only clearing.

#### Scenario: Reset a running instance

- **WHEN** the caller changes registers and RAM, executes a step, and requests facade reset
- **THEN** the same instance resumes at its reset vector with repeated-reset effects and unchanged RAM and cycles
- **AND** one completed CPU reset event is available without a duplicate reset or instruction event

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

When frame output is enabled, each vblank entry SHALL publish one native-size frame for the visible period
that just ended. The host SHALL be able to present the most recent completed frame.

#### Scenario: Publish with NMI generation disabled

- **WHEN** a program leaves PPUCTRL bit 7 clear and changes the backdrop color between two vblank entries
- **THEN** the host can present one completed frame at each entry
- **AND** the second frame shows the updated color

#### Scenario: Publish before the interrupt updates video memory

- **WHEN** a program writes a color during its vblank NMI handler
- **THEN** the captured frame at the interrupt boundary has the previous color
- **AND** the next completed frame can present the updated color
