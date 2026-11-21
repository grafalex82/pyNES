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
