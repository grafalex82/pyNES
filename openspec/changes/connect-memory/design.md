# Design

## Context

See [proposal.md](proposal.md) and [the cpu-memory spec](specs/cpu-memory/spec.md).
The archived loader change provides NESFile getters, synthetic-file tests, pytest configuration, and `misc/nesinfo.py`.
There is no RAM, ROM device, Machine, or CPU implementation yet. Inspected local files declare mapper/submapper 0,
no trainer, and either 16384 or 32768 PRG bytes, so both ordinary NROM layouts are immediately relevant.

This design is needed because three new components establish the address-routing boundary used by the future CPU.
The existing file-inspection contract remains unchanged.

## Goals / Non-Goals

**Goals:**

- Make device-relative offsets distinct from CPU addresses.
- Give the future CPU one byte-oriented read/write interface through Machine.
- Explain aliasing with one physical RAM buffer and fixed PRG wiring.

**Non-Goals:**

- CPU fields, reset methods, word helpers, instruction dispatch, or an emulator CLI.
- A generic bus registry, device base class, or mapper framework before another device actually needs one.
- Validation of malformed files, invalid addresses/values, exception presentation, or header repair.

## Decisions

### Keep memory devices simple and independent

Add RAM in `src/ram.py` and ROM in `src/rom.py`. RAM takes a byte count and owns a private bytearray.
ROM takes already parsed PRG bytes and keeps immutable private data. Both devices expose `read_byte(offset)`
and `write_byte(offset, value)`. ROM writes raise PermissionError. Neither device knows CPU ranges, mirroring, files,
or Machine. Use private fields consistently with NESFile; consume its parsed values only through existing getters.

A common method shape is sufficient without an abstract interface. A shared writable memory class would blur the ROM
write policy. Plain byte access also avoids introducing stack, word, or burst APIs before their behavior is needed.

### Assemble the initial supported configuration in Machine

Add Machine in `src/machine.py`, constructed from an already parsed NESFile. Its constructor reads mapper, submapper,
trainer, and PRG getters, creates RAM(2048) and ROM(PRG bytes), and stores both privately. No file is reread and no CPU
is constructed. Expose `read_byte(address)` and `write_byte(address, value)` to future CPU callers.

Support mapper/submapper 0, PRG sizes 16384 or 32768, and an empty trainer. Raise NotImplementedError for other values,
identifying the unsupported feature. These are limits of the chosen cartridge wiring, not file-integrity checks.
Trainer placement and cartridge RAM need their own behavior later; do not silently discard a trainer or allocate
extra RAM now. CHR and video metadata stay in NESFile and are not connected to CPU memory by this change.

Taking NESFile keeps the initial configuration in one place and uses the actual loader interface. A separate factory
or dependency-injection layer is unnecessary for this single configuration; tests can supply synthetic NESFile inputs.

### Route addresses instead of duplicating memory

| CPU address | Destination | Device offset |
| --- | --- | --- |
| $0000-$1FFF | One 2048-byte RAM buffer | address AND $07FF |
| $2000-$7FFF | NotImplementedError for reads and writes | No device connected yet |
| $8000-$FFFF | PRG ROM | (address - $8000) AND (PRG byte size - 1) |

The RAM mask models repeated address wiring; it does not create copies that need synchronization. The PRG mask
selects one 16 KiB image twice or one complete 32 KiB image. Test both layouts with different bytes at key boundaries.
These ranges follow the [CPU memory map](https://www.nesdev.org/wiki/CPU_memory_map) and
[NROM mapping](https://www.nesdev.org/wiki/NROM). Mapper 0 has no writable bank-selection registers. Writes in its
PRG window reach ROM and raise PermissionError according to the diagnostic policy below. Bus-conflict signals and
physical timing are not modeled.

Direct fixed routing is sufficient for NROM, with no bank-switching state. When a later cartridge needs banking, its
bank state can belong to that cartridge component while CPU requests continue to enter through Machine.

### Raise an error on ROM writes

ROM.write_byte raises the built-in PermissionError before changing any data. Machine delegates PRG-window writes to
ROM and lets that exception propagate unchanged. NotImplementedError remains reserved for missing behavior.

At the user's request, this is a diagnostic trap: ordinary NROM writes do not alter ROM or bank state, whereas this
emulator will stop with an exception. Record this deliberate departure in `doc/decisions.md` and test both direct ROM
writes and writes through Machine. No custom exception type or error-handling layer is needed.

### Start RAM deterministically and document the difference

Use zero-filled RAM when a new Machine is constructed. Real power-up RAM contents are not a reliable software contract;
see [CPU power-up state](https://www.nesdev.org/wiki/CPU_power_up_state). Zero filling makes runs and tests repeatable
without adding a randomization option. Record this explicit initialization convenience in `doc/decisions.md`.
There is no reset operation in this change, so do not accidentally define whether reset clears or preserves RAM.
Zero-filled RAM and the ROM-write trap are deliberate departures in this change; no game bytes are patched.

### Keep missing behavior separate from ROM write errors

Unconnected reads and writes raise NotImplementedError containing the operation and CPU address. Do not fake register
responses, model open-bus values, or treat the rest of the CPU space as RAM. These exceptions mark future work rather
than claim the real console has no device there. Valid byte values and CPU addresses are assumed; native storage
failures can propagate. ROM-write PermissionError also propagates unchanged. No redundant range checks, recovery
paths, or exception wrappers are required.

## Risks / Trade-offs

- Zero-filled RAM differs from hardware power-up variability -> Document it as an initialization convenience.
- Four RAM windows may be mistaken for four buffers -> Verify writes through every alias share one value.
- A 32 KiB cartridge might accidentally mirror its lower half -> Use distinct upper/lower data and boundary assertions.
- ROM writes now stop execution instead of being ignored -> Document the diagnostic trap as a hardware departure.
- File parsing supports more cartridges than this memory model -> Keep construction limits explicit and separate.
- New routing may be mistaken for a runnable emulator -> Document byte access only; CPU reset/execution stay absent.

## Migration Plan

Add device and routing modules plus focused tests, using the existing pytest setup. Update system documentation and
current-state notes without changing the loader API, inspection output, or local ROM contents. Reverting these additions
restores the file-inspection-only state. No data migration or new dependency is needed.
