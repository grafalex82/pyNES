# Proposal

## Why

The selected CPU instructions extend the educational emulator in small, understandable steps.
At the user's request, their plans are collected into one reviewable OpenSpec change.

## What Changes

- Add JMP absolute and indirect, JSR, and RTS.
- Add STA, STX, STY, LDA, LDX, and LDY using zero-page addressing.
- Add STA and LDA using absolute,X and absolute,Y; add LDX absolute,Y and LDY absolute,X.
- Add accumulator ASL, LSR, ROL, and ROR; add immediate CMP, CPX, and CPY.
- Add immediate AND, ORA, and EOR; add STA with indexed-indirect and indirect-indexed addressing.
- Keep other unsupported opcodes explicit and preserve existing execution and trace conventions.
- Implement and verify one encoding at a time; report the next observed obstacle and stop at that boundary.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- cpu-execution: execute the 28 selected control-flow, memory, shift, rotate, comparison, and logical encodings.

## Impact

CPU dispatch and execution, focused synthetic pytest cases, and explanatory documentation will change.
No cartridge patch, unrelated instruction, new component, or cycle-accurate hardware model is included.
