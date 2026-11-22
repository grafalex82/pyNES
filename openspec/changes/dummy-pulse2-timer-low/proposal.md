# Proposal

## Why

Super Mario Bros. reaches an unimplemented $4006 write while transitioning to a level. Learn the role of the
second pulse channel's timer register and extend the existing silent APU boundary by this one register.

## What Changes

- Accept writes to $4006 through Machine and the dummy APU, logging the ignored value.
- Keep reads and other unimplemented registers explicit; do not implement timer state or audio.
- Verify with synthetic tests and rerun the identified ROM to find the next obstacle.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `apu-registers`: Accept the pulse 2 timer-low write without audio effects.
- `cpu-memory`: Route this write to the APU while retaining unsupported reads.

## Impact

Machine routing, the APU dummy, focused tests, and the memory and decision documentation change.
