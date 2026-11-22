# Graphical Cartridge Run

## ADDED Requirements

### Requirement: Open the video window on cartridge startup

With only a cartridge path, the entry point SHALL open one 768 × 720 video window after loading the cartridge
and before executing its first instruction. A usage request with `--help` SHALL exit without opening a window.

#### Scenario: Start with only a cartridge path

- **WHEN** a caller runs `python main.py cartridge.nes` with a supported cartridge
- **THEN** the 768 × 720 window opens before its first instruction executes

#### Scenario: Request help without opening the display

- **WHEN** a caller runs `python main.py --help`
- **THEN** usage is printed and the display is not initialized

### Requirement: Present completed game frames and process close events

The host SHALL present completed 256 × 240 game frames at scale three. It SHALL process window events between
bounded execution blocks and release the display on window close or when an execution exception propagates.

#### Scenario: Show a frame and close the window

- **WHEN** a supported synthetic cartridge produces a frame and a window-close event is received
- **THEN** the frame is presented at the specified scale and the event ends the loop and releases the display

#### Scenario: Release the display on execution failure

- **WHEN** a cartridge encounters unsupported execution behavior with the window open
- **THEN** the display is released and the error propagates with its traceback

## MODIFIED Requirements

### Requirement: Make instruction traces visible in the console

Application startup SHALL disable logging by default. With `--debug`, it SHALL enable DEBUG logging to the console
before CPU initialization. The log SHALL include reset completion and completed-instruction lines with their
specified layout and CYC totals. Console instruction lines SHALL start at the address column without level,
logger-name, or timestamp prefixes. Device and CPU components SHALL leave logging configuration to the application.

#### Scenario: Run without logging

- **WHEN** the application executes SEI at $8000 without `--debug`
- **THEN** no reset or instruction log is printed

#### Scenario: Observe the first completed instruction

- **WHEN** the application executes SEI at $8000 after startup with `--debug`
- **THEN** the line begins with address 8000, byte 78, and mnemonic SEI in their fixed columns
- **AND** state starts at column 44 and reports PC=8001, I set, and CYC=2
- **AND** the reset event precedes the completed-instruction event

### Requirement: Stop naturally at missing behavior

Filesystem, parsing, unsupported-cartridge, and execution exceptions SHALL propagate without custom recovery,
traceback suppression, automatic skipping, or retries. A failed instruction SHALL terminate the console run with
an unsuccessful exit and its ordinary traceback. With `--debug`, traces for earlier instructions remain visible.

#### Scenario: Continue through CLD to the next unsupported opcode

- **WHEN** the selected program begins with SEI at $8000, CLD at $8001, and unsupported $02 at $8002 with `--debug`
- **THEN** aligned SEI and CLD traces show CYC=2 and CYC=4 before the process exits unsuccessfully
- **AND** the traceback identifies NotImplementedError for opcode $02 at $8002
