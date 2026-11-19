# Proposal

## Why

The first instructions of the three local ROMs require register loads, stores, a stack transfer, a branch,
and an index decrement that are not yet implemented.

## What Changes

- Add immediate and absolute LDA/LDX/LDY and absolute STA/STX/STY.
- Add implied TSX, TXS, DEX, and DEY, and relative BPL.
- Preserve explicit errors for all other unimplemented opcodes and addressing forms.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cpu-execution`: execute the selected opcodes, preserve traces, and update unsupported-opcode examples.

## Impact

Change CPU dispatch, synthetic tests, execution documentation, and the decision record. Apply after the
ppu-register-writes package. The user explicitly requested these instruction families as one package.
