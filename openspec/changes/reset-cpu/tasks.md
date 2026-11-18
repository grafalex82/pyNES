# Tasks

## 1. CPU state interface

- [x] 1.1 Add private CPU registers and seven boolean flag properties including `break_flag` in `src/cpu.py`; keep
  no packed P state and extend the two packing/unpacking tests for B=$10, bit 5 normalization, and all-set P=$FF.
  Assert 8-bit/16-bit ranges in register setters and verify endpoints and unchanged state after rejected values.
- [x] 1.2 Explain register widths, the seven boolean variables, and NV1BDIZC packing/unpacking in `doc/cpu.md`;
  distinguish software B from the six hardware flags and verify that bit 5 has no stored variable.

## 2. Startup and repeated reset

- [x] 2.1 Initialize CPU through one reset after constructor-only register/flag initialization; verify initial
  registers and flags, little-endian PC, ordered Machine vector reads, and unchanged RAM for both PRG sizes.
- [x] 2.2 Implement repeated reset; verify preserved A/X/Y and C/Z/B/D/V/N, SP wrap and successive decrements, a reread
  vector, unchanged stack/RAM, and no opcode fetch even when the new vector targets an unimplemented device address.
- [x] 2.3 Add `log_state(event)` to log event text, hexadecimal A/X/Y/SP/PC, and a symbolic NV1BDIZC status mask;
  use it for one completed reset event. Verify custom event text, each flag, constant bit 5, and resulting register
  values with caplog for startup and repeated reset, without configuring handlers or adding instruction tracing.
- [ ] 2.4 Record separate flag storage, the software B convention, initial state, and omitted bus reads/timing;
  explain B initialization/preservation as a hardware departure in `doc/decisions.md` and its effect on displayed P;
  update status notes and CPU documentation, verifying CPU reset remains distinct from full-console reset/execution.

## 3. Integration checks

- [ ] 3.1 Run `python -m pytest`; verify new CPU tests and existing memory/loader/inspection tests pass with synthetic
  data, unchanged memory and inspection contracts, and no dependency on local game files.
- [ ] 3.2 Run `openspec validate reset-cpu --strict --no-interactive` and text checks; verify strict validation,
  120-character lines, and scope limited to register state/reset with no instruction or execution-loop implementation.
