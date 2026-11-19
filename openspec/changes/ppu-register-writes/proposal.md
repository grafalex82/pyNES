# Proposal

## Why

All three local ROMs write PPUCTRL and poll PPUSTATUS, but Machine currently rejects every PPU access.

## What Changes

- Introduce a minimal PPU component and route writes to its eight registers and mirrors.
- Retain written bytes for inspection only and return alternating $00/$80 from status reads.
- Keep other reads and all rendering, timing, interrupts, and register effects unimplemented.

## Capabilities

### New Capabilities

- `ppu-registers`: minimal CPU-visible PPU register access.

### Modified Capabilities

- `cpu-memory`: route PPU-window writes and status reads.
- `cpu-execution`: move the unconnected opcode-fetch example away from PPUSTATUS.

## Impact

Add a PPU module; change Machine, tests, memory documentation, and the decision record.
This user-requested package groups the two related PPU behaviors into one change.
