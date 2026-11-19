# Proposal

## Why

CPU reset now reaches a program's entry address, but there is no instruction execution or application entry point.
Execute selected implied instructions through a small Emulator facade to reach the first instruction and next obstacle.

## What Changes

- Add CPU.step() for CLC ($18), SEC ($38), CLI ($58), SEI ($78), CLD ($D8), SED ($F8), CLV ($B8), and NOP ($EA).
- Add a read-only cumulative CPU cycles counter; each selected instruction adds two cycles after completion.
- Keep every other opcode explicit with NotImplementedError containing its byte and instruction address.
- Log each completed instruction in aligned address/bytes/mnemonic/operand columns, followed by log_state() output.
- Keep post-execution registers, symbolic flags, and cumulative cycles together at the end of each trace line.
- Add Emulator as the UI's execution boundary, with step(), run(cycles), and a shared reset() entry point.
- Bound each run by elapsed CPU cycles through the same single-step path; reserve breakpoints for a later change.
- Complete the last instruction even if it exceeds the requested cycle budget; measure each call from its entry count.
- Add root main.py to accept a ROM path, configure components/logging, and repeatedly run cycle-budgeted blocks.
- Stop naturally at the first unimplemented behavior; retain tracebacks and the already completed instructions.
- Explain SEI, the control flow, and the first observed instructions in the two target ROM listings.

The user expanded this change to the eight selected encodings and nominal instruction-cycle accounting. Keep a separate
implementation task per instruction so each can be understood and checked individually. The facade and console loop
complete the entry path; device scheduling, interrupts, other opcodes, and the graphical UI remain future work.

## Capabilities

### New Capabilities

- `cpu-execution`: Machine-routed fetch, selected flag instructions and NOP, cycle accounting, diagnostics, and tracing.
- `emulator-control`: A shared UI facade for one instruction, cycle-budgeted execution, and reset coordination.
- `emulator-cli`: Cartridge selection and application startup with a console emulation loop.

### Modified Capabilities

None. The existing cartridge inspection and memory contracts remain unchanged. CPU state and reset follow the
implemented reset-cpu change, including properties, separately stored flags, and the software B inspection convention.

## Impact

- Extend src/cpu.py; add src/emulator.py and root main.py without changing Machine's memory-only constructor.
- Add focused CPU, facade, and console cases using synthetic cartridges; keep logging assertions in logger-only tests.
- Instruction tests cover behavior and cycles without checking logger calls, records, or instruction trace text.
- Update README.md, doc/development.md, doc/cpu.md, and doc/decisions.md; add concise execution documentation.
- Begin only the verified entry-instruction rows under doc/disassembly/, with ROM identities and byte locations.
- Build on the implemented cpu-reset specification and the archived reset-cpu change.
- Use only the existing standard library and pytest; no new runtime dependency or packaging configuration.
- Selected reset behavior: Emulator.reset() preserves Machine, RAM, and accumulated instruction cycles via CPU.reset().
  The counter starts at zero on construction; functional reset contributes no cycles. Device reset coordination grows
  when devices exist, without changing reset into another power-on.
