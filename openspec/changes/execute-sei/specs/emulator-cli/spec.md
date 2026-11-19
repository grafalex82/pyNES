# Spec Delta

## Purpose

Start emulation from a user-selected local cartridge in a console application, exposing completed instruction traces
and the next missing behavior. This initial host loop will later be replaced by a graphical application using the
same execution facade. Cartridge inputs are assumed structurally valid; errors need no recovery or custom presentation.

## ADDED Requirements

### Requirement: Accept the cartridge path from the command line

The console entry point SHALL accept one positional NES file path and provide standard help output.
Relative paths SHALL resolve against the caller's working directory, including quoted paths containing spaces.
The entry point SHALL also be runnable by its absolute path from another working directory without installation
or a configured module search path.

#### Scenario: Select a cartridge outside the repository

- **WHEN** a caller runs the entry script by absolute path with a quoted relative cartridge path containing spaces
- **THEN** the selected file is loaded relative to the caller's directory and connected using existing cartridge support

#### Scenario: Request usage information

- **WHEN** the entry script is run with --help
- **THEN** it prints usage and exits without reading a cartridge or starting emulation

### Requirement: Initialize the system and repeat bounded execution

The application SHALL load and parse the supplied cartridge, connect its supported memory configuration, and
initialize the facade and CPU once before entering a loop of blocks bounded by CPU cycle budgets.
It SHALL call the facade for execution, with no implicit reset between blocks or independent UI opcode handling.

#### Scenario: Reach and pass the first instruction

- **WHEN** a supported cartridge has a reset vector pointing to SEI followed by an unsupported opcode
- **THEN** application startup reaches the entry address, SEI executes once, and execution attempts the next instruction
- **AND** only one CPU startup reset occurs

#### Scenario: Continue after the first cycle budget is consumed

- **WHEN** the selected synthetic program contains 501 two-cycle NOPs followed by unsupported $A9
- **THEN** the first 1000-cycle block completes after 500 NOPs and the application starts another block
- **AND** the next NOP completes at CYC=1002 before $A9 stops execution, with no intervening reset

### Requirement: Make instruction traces visible in the console

Application startup SHALL enable CPU DEBUG logging to the console before CPU initialization.
The log SHALL include reset completion and completed-instruction lines with their specified layout and CYC totals.
Console instruction lines SHALL start at the address column without level, logger-name, or timestamp prefixes.
Device and CPU components SHALL leave logging configuration to the application.

#### Scenario: Observe the first completed instruction

- **WHEN** the application executes SEI at $8000 after startup
- **THEN** the line begins with address 8000, byte 78, and mnemonic SEI in their fixed columns
- **AND** state starts at column 44 and reports PC=8001, I set, and CYC=2
- **AND** the reset event precedes the completed-instruction event

### Requirement: Stop naturally at missing behavior

Filesystem, parsing, unsupported-cartridge, and execution exceptions SHALL propagate without custom recovery,
traceback suppression, automatic skipping, or retries. A failed instruction SHALL terminate the console run with
an unsuccessful exit and its ordinary traceback, retaining traces for earlier completed instructions.

#### Scenario: Continue through CLD to the next unsupported opcode

- **WHEN** the selected program begins with SEI at $8000, CLD at $8001, and unsupported $A9 at $8002
- **THEN** aligned SEI and CLD traces show CYC=2 and CYC=4 before the process exits unsuccessfully
- **AND** the traceback identifies NotImplementedError for opcode $A9 at $8002
