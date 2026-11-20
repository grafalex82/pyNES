# Proposal

## Why

The identified Battle City ROM stops on a write to $4017 after reaching the existing dummy APU. Accepting this one
write as an explicitly documented approximation allows the next missing behavior to be observed without implementing
the APU frame sequencer.

## What Changes

- Accept CPU writes to $4017 through the existing dummy APU without frame-counter or IRQ effects.
- Keep CPU reads from $4017 unsupported because they address controller 2, not the APU.
- Verify direction-sensitive routing and document the hardware behavior and approximation.
- Recheck the observed Battle City obstacle and report the next one without implementing it.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cpu-memory`: Route writes, but not reads, at $4017 to the existing dummy audio component.

## Impact

- Existing APU and Machine routing, focused synthetic tests, and memory/decision documentation.
- No sound, frame timing, controller, interrupt implementation, or ROM patch.
- The implemented `add-dummy-apu-registers` change has not yet been archived; its CPU-memory delta must be synced or
  archived before this change is archived, so its earlier routing changes are not overwritten.
