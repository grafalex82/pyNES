# Proposal

## Why

The selected control-flow and memory instructions extend the educational CPU in small, understandable steps.
At the user's request, their plans are collected into one reviewable OpenSpec change.

## What Changes

- Add JMP absolute and indirect, JSR, and RTS.
- Add STA, STX, STY, LDA, LDX, and LDY using zero-page addressing.
- Add STA and LDA using absolute,X and absolute,Y; add LDX absolute,Y and LDY absolute,X.
- Keep other unsupported opcodes explicit and preserve existing execution and trace conventions.
- Implement and verify one encoding at a time; report the next observed obstacle and stop at that boundary.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- cpu-execution: execute the 16 selected control-flow, zero-page, and indexed-absolute encodings.

## Impact

CPU dispatch and execution, focused synthetic pytest cases, and explanatory documentation will change.
No cartridge patch, unrelated instruction, new component, or cycle-accurate hardware model is included.
