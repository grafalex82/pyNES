# Proposal

## Why

Studying game code requires a readable view of PRG ROM independently of the instructions the emulator can execute.
A small offline listing utility provides that prerequisite while making the limits of automatic disassembly visible.

## What Changes

- Add a standalone script in `misc/` that takes a NES file and an output path and produces a text listing.
- Decode official 6502 instructions in two linear passes, using `db` for other bytes and labels for direct targets.
- Use CPU addresses for mapper-0 PRG, symbolic peripheral registers, and `EQU` for aliases and non-line targets.
- Support the ordinary 16 KiB and 32 KiB fixed PRG layouts without changing CPU execution or emulated hardware.
- Document that code and data cannot reliably be distinguished by this linear scan.

## Capabilities

### New Capabilities

- `nes-disassembly`: Offline, two-pass mapper-0 PRG listings with instructions, labels, and hardware symbols.

### Modified Capabilities

None.

## Impact

- Add a Python utility and focused synthetic pytest cases, reusing the existing `NESFile` parser.
- Update usage and decision documentation; no new dependencies, game patches, or emulator behavior are introduced.
- Generated listings are a starting point for study, not verified or reassemblable game disassemblies.
