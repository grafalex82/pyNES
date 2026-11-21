# Proposal: Complete the official NES CPU opcodes

## Why

The CPU executes 129 of the 151 official NES encodings. The local Super Mario Bros. image stops at `INC absolute`
(`$EE`) at `$804C`. Use one plan for the remaining encodings while implementing and verifying one opcode at a time.

## What Changes

- Add the absolute and absolute,X forms of `INC` and `DEC`.
- Add the `(zp,X)` and `(zp),Y` forms of `AND`, `ORA`, `EOR`, `ADC`, `SBC`, and `CMP`.
- Add `PHA`, `PLA`, `PHP`, `PLP`, `BRK`, and `RTI`.
- Leave behavior of existing encodings and devices unchanged. Do not implement unofficial opcodes or external
  IRQ/NMI delivery, or modify cartridge data.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cpu-execution`: Add one requirement per remaining official encoding, with nominal cycles and observable effects.

## Impact

`src/cpu.py`, focused cases in `test/test_cpu.py`, and the decision record. No public API or dependency changes.
