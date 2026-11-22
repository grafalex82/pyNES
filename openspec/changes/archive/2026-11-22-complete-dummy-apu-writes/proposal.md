# Proposal

## Why

Games can initialize or read different APU addresses, but the current partial dummy stops at many of them. Completing
the silent CPU-facing boundary avoids repeating the same stub change for each register and makes its limitations clear.

## What Changes

- Accept and ignore writes at $4000-$4013, $4015, and $4017, including the unused $4009 and $400D addresses.
- Return $00 for reads at $4000-$4013 and $4015 as a documented approximation of open bus and inactive status.
- Preserve sprite DMA at $4014, controller accesses at $4016 and controller 2 reads at $4017.
- Do not implement audio, register state, open bus, DMC transfers, frame sequencing, or audio interrupts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `apu-registers`: Complete the silent register write and fixed read boundary.
- `cpu-memory`: Route the selected accesses while preserving neighboring devices and unsupported addresses.

## Impact

Machine routing, the APU component, focused synthetic tests, and the memory and decision documentation are affected.
No ROM changes or new dependencies are planned.
