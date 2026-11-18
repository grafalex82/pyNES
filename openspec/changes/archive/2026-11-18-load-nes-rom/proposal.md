# Proposal

## Why

The project needs a small way to inspect a CLI-selected NES file before memory mapping or CPU execution exists.
The loader will make the cartridge header and byte sections available for the next incremental changes.

## What Changes

- Add `misc/nesinfo.py` to print the format, mapper/submapper, ROM and trainer sizes, and basic header flags.
- Add a reusable parsed-file object for ordinary iNES and NES 2.0 headers and trainer/PRG/CHR data.
- Explicitly reject declared format features that are not implemented yet.
- Assume valid input: do not add corruption checks, header repair, or friendly exception handling.
- Verify valid-file parsing and inspection with synthetic ROMs; retain ordinary Python failures for invalid input.

Scope ends at file inspection. CPU, RAM/ROM devices, Machine, mapper emulation, and instructions remain later changes.

## Capabilities

### New Capabilities

- `nes-rom-loading`: Read NES cartridge metadata and byte sections and inspect them with a small standalone utility.

### Modified Capabilities

None; the main specification inventory is empty.

## Impact

- Add `src/nesfile.py`, `misc/nesinfo.py`, focused tests, and minimal pytest setup.
- Update usage documentation, the decision record, and project guidance about assuming valid input.
- Runtime code uses the standard library; pytest is needed only for tests.
- Keep local ROM contents unchanged and leave emulator startup for a later change.
