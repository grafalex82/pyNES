# Tasks

## 1. Direction-sensitive APU stub

- [x] 1.1 Route CPU writes at $4017 to APU offset $17 and accept them without effects; verify representative values,
  routing, unchanged $4015 status, and existing DEBUG logging with focused pytest cases.
- [x] 1.2 Preserve unsupported CPU reads at $4017 and direct APU reads at offset $17; verify their errors identify
  the operation and address or offset, and verify adjacent unsupported addresses remain unsupported.
- [x] 1.3 Add a synthetic CPU program that writes $4017 and continues; verify it and the existing APU tests pass.
- [x] 1.4 Update the relevant memory map and decision documentation to describe hardware behavior and the ignored
  write; verify descriptions distinguish controller reads and do not claim frame timing or IRQ support.

## 2. Bounded integration check

- [x] 2.1 Run focused pytest coverage and, if the identified local Battle City ROM is available, repeat the bounded
  attempt; record the next observed obstacle or report why the ROM check could not run, without implementing it.

## Workflow follow-up

- Before archiving this change, sync or archive `add-dummy-apu-registers` so its earlier CPU-memory delta is retained.
