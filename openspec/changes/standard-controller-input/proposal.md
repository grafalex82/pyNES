# Proposal

## Why

The controller ports currently return a fixed zero, so games cannot receive player input. Implementing standard
controller polling connects an observable NES peripheral behavior to a simple host keyboard mapping.

## What Changes

- Replace the controller stubs with two independently readable standard NES controllers sharing the $4016 strobe.
- Map the agreed keyboard keys to their buttons and release held buttons when the window loses focus.
- Preserve the existing APU frame-counter write at $4017, and document the simplified controller read bus bits.
- Keep physical gamepads, configurable bindings, other controller types, and unrelated peripheral behavior out of scope.

## Capabilities

### New Capabilities

- `standard-controller-input`: Standard controller polling and fixed host keyboard input for two players.

### Modified Capabilities

- `cpu-memory`: Route controller port accesses instead of returning the temporary stub responses.

## Impact

Machine routing, a separate controller component, the pygame event loop, controller and CLI tests, and project
documentation will change. The existing pygame dependency remains sufficient; no ROM patches are planned.
