# Tasks

## 1. Add instructions individually and count their cycles

Complete instruction tasks one at a time and verify the effect specified by each task. Task 1.10 covers cycle
increments for every selected opcode. Instruction tests do not capture logs or assert logger calls, record counts,
trace text, or alignment.

- [x] 1.1 Add CPU.step() for implied SEI ($78). Write $78 to RAM at $0000 and verify I is set from either initial value.
- [x] 1.2 Add CLC ($18); verify C becomes false from either initial value while other state is preserved.
- [x] 1.3 Add SEC ($38); verify C becomes true from either initial value while other state is preserved.
- [x] 1.4 Add CLI ($58); verify I becomes false from either initial value with other state preserved and no IRQ logic.
- [x] 1.5 Add CLD ($D8); verify D becomes false from either initial value while other state is preserved.
- [x] 1.6 Add SED ($F8); verify D becomes true from either initial value without adding decimal arithmetic.
- [x] 1.7 Add CLV ($B8); verify V becomes false from either initial value while other state is preserved.
- [x] 1.8 Add official NOP ($EA); verify PC advances while A/X/Y/SP, every flag, and memory remain unchanged.
- [x] 1.9 Keep unsupported opcodes and fetch failures explicit; verify $A9 and unofficial NOP $1A diagnostics,
  unchanged failed-step state, and retained partial progress before the next unsupported instruction.
- [x] 1.10 Add read-only CPU.cycles initialized to zero; verify each selected encoding adds two, including idempotent
  flag changes and NOP, mixed execution adds correctly, counters are independent, and reset/failure add nothing.
- [ ] 1.11 Add aligned tracing through log_instruction() and log_state(); review post-execution wiring and keep small
  direct-helper cases in test/test_cpu_logging.py for layout, blank operands, state/CYC, and observational behavior.
  Move existing reset/log_state logging-only cases there and update CYC expectations; add no per-instruction log tests.
- [ ] 1.12 Update doc/cpu.md and doc/decisions.md with the eight encodings, trace layout, cycle/reset rules, and timing
  omissions; begin SEI/CLD listing rows with ROM identities and CPU/PRG/file offsets verified against source bytes.

## 2. Add the shared Emulator control interface

- [ ] 2.1 Add Emulator(machine), its read-only cpu property, and step() in src/emulator.py; verify one startup,
  no instruction during construction, preserved RAM, independent CPU/cycle state, and exactly one delegated step.
- [ ] 2.2 Add run(cycles) through self.step() using the CPU.cycles delta at call entry; verify budgets 0/1/2/3/6,
  nonzero entry counters, whole-instruction overshoot, independent successive budgets, and partial progress on failure.
- [ ] 2.3 Add reset() through CPU.reset(); verify preserved Machine/RAM/cycles and repeated-reset PC/SP/flags,
  without reconstruction, duplicate reset, instruction execution, or assertions about logging.
- [ ] 2.4 Add doc/execution.md and a decision entry on ownership, controls, cycle budgets, overshoot, and cycle totals;
  explain future breakpoint placement and verify the documented API matches tests without breakpoint placeholders.

## 3. Start execution from the console

- [ ] 3.1 Add main.py with one ROM argument, script-relative imports, message-only logs, and 1000-cycle run() calls;
  verify --help, spaced paths from another directory, and the expected $A9 exception/address without log assertions.
- [ ] 3.2 Add a bounded subprocess case with 501 NOPs from $8000 followed by $A9; verify an unsuccessful exit and
  NotImplementedError for $A9 at $81F5 after crossing the first cycle block, without inspecting instruction traces.
- [ ] 3.3 Document the console command and supported-entry stop in doc/execution.md, README.md, and doc/development.md;
  record console/logging decisions and verify the example against a synthetic ROM without games.

## 4. Check the complete ROM-to-instruction path

- [ ] 4.1 Run python -m pytest, strict OpenSpec validation, and style checks; verify existing and new contracts pass,
  lines stay within 120 characters, and opcode support is limited to the eight requested encodings.
- [ ] 4.2 Run both identified target images through main.py; verify BattleCity executes SEI for two cycles and stops at
  $C071:$A9, while the 32 KiB image executes SEI/CLD for four cycles and stops at $8002:$A9. Verify unchanged hashes,
  record observed traces and cycle totals, and stop without implementing $A9, peripherals, or ROM patches.
