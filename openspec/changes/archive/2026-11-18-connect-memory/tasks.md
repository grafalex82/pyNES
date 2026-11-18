# Tasks

## 1. Memory devices

- [x] 1.1 Add RAM in `src/ram.py`; verify zero initialization, byte access, boundaries, and instance isolation in
  `test/test_ram.py` using valid offsets; verify out-of-range byte values raise ValueError without changing RAM.
- [x] 1.2 Add ROM in `src/rom.py`; verify source-byte reads, write PermissionError, and unchanged data in
  `test/test_rom.py`.
- [x] 1.3 Explain device-relative offsets and ROM write errors in comments; record zero-filled RAM and the diagnostic
  ROM-write trap as deliberate departures in `doc/decisions.md`, and verify the explanation matches device tests.

## 2. Machine routing

- [x] 2.1 Add Machine using existing NESFile getters; verify `test/test_machine.py` covers RAM aliases, independent
  configurations, both PRG layouts, and propagation of ROM write PermissionError without constructing a CPU.
- [x] 2.2 Keep unconnected addresses and unsupported cartridge configurations explicit; verify parameterized read/write
  and construction tests check NotImplementedError diagnostics without adding malformed-input validation.
- [x] 2.3 Explain the CPU memory map and supported limits in `doc/memory.md` and update relevant current-state notes;
  verify a synthetic byte-access example and keep CPU reset/execution described as future work.

## 3. Integration checks

- [x] 3.1 Run `python -m pytest`; verify all new memory tests and existing loader/inspection tests pass using synthetic
  files, with no dependency on local game ROMs and no change to NESFile getters or CLI output.
- [x] 3.2 Run `openspec validate connect-memory --strict --no-interactive` and check edited text formatting; verify
  validation passes, lines stay within 120 characters, and no CPU/reset/instruction behavior has entered this change.
