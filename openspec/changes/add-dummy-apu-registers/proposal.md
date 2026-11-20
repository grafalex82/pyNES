# Proposal

## Why

Bounded checks of the identified Battle City and Super Mario Bros. cartridges stop on writes to $4015 and $4011,
respectively. A small, explicitly approximate APU boundary lets this register-access behavior be studied without
implementing audio or claiming that either game runs.

## What Changes

- Accept CPU writes to $4010-$4013 and $4015 without implementing audio effects.
- Return $00 on CPU reads from those addresses, including an always-inactive $4015 status.
- Keep $4014 DMA and all other unimplemented addresses explicit; do not implement DMC playback or IRQs.
- Document and verify the approximation, then report the next observed obstacle without implementing it.

## Capabilities

### New Capabilities

- `apu-registers`: Minimal CPU-visible APU register accesses with a deterministic inactive status approximation.

### Modified Capabilities

- `cpu-memory`: Route the selected APU addresses through a separate device instead of rejecting them.

## Impact

- A new audio component and Machine routing, with focused synthetic tests.
- CPU memory documentation, current-state documentation, and the decision record.
- No dependencies, ROM patches, audio output, or claim of game playability.
