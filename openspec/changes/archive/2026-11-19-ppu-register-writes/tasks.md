# Tasks

## 1. Register writes

- [x] 1.1 Add a per-Machine PPU and mirrored writes; verify retained bytes, all offsets, and independent instances.
- [x] 1.2 Verify writes to $2002 and mirrors are retained without hardware effects; keep unsupported reads explicit.
- [x] 1.3 Update memory tests and docs; record the register-write and warmup departures in the decision record.

## 2. Status reads

- [x] 2.1 Add $00/$80 status alternation; test first value, repeated reads, mirrors, and independent PPU instances.
- [x] 2.2 Verify writes do not advance the sequence, CPU reset preserves PPU state, and other reads fail explicitly.
- [x] 2.3 Update affected $2002 failure tests and record the read-driven approximation and affected ROMs.

## 3. Integration

- [x] 3.1 Run focused and full pytest suites and validate this change in strict mode.
- [x] 3.2 Attempt applicable local ROMs with a bounded cycle budget; report the next obstacle without implementing it.

## Workflow follow-up

- Review and archive this change before applying the CPU instruction package.
