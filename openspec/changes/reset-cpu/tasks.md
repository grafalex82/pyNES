# Tasks

## 1. CPU state interface

- [ ] 1.1 Add private CPU registers and six separate boolean flags in `src/cpu.py`; keep no packed P state and verify
  register access plus get_p()/set_p() conversion with single-bit, combined, and successive-clearing test cases.
- [ ] 1.2 Explain register widths, the six boolean variables, and P packing/unpacking in `doc/cpu.md`; verify the
  documented bit layout matches the tests and stores neither a packed byte nor B/unused-flag variables.

## 2. Startup and repeated reset

- [ ] 2.1 Initialize CPU through one reset after constructor-only register/flag initialization; verify initial
  registers and flags, little-endian PC, ordered Machine vector reads, and unchanged RAM for both PRG sizes.
- [ ] 2.2 Implement repeated reset; verify preserved A/X/Y and C/Z/D/V/N, SP wrap and successive decrements, a reread
  vector, unchanged stack/RAM, and no opcode fetch even when the new vector targets an unimplemented device address.
- [ ] 2.3 Log one completed reset event with the CPU component logger; verify all resulting register values with
  caplog for startup and repeated reset, without configuring handlers or adding instruction tracing.
- [ ] 2.4 Record separate flag storage, the initial profile, and omitted dummy reads/timing in `doc/decisions.md`;
  update status notes and CPU documentation, verifying CPU reset remains distinct from full-console reset/execution.

## 3. Integration checks

- [ ] 3.1 Run `python -m pytest`; verify new CPU tests and existing memory/loader/inspection tests pass with synthetic
  data, unchanged memory and inspection contracts, and no dependency on local game files.
- [ ] 3.2 Run `openspec validate reset-cpu --strict --no-interactive` and text checks; verify strict validation,
  120-character lines, and scope limited to register state/reset with no instruction or execution-loop implementation.
