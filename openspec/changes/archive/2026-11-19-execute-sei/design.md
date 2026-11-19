# Design

## Context

See [the proposal](proposal.md#why) for motivation and the three [execution](specs/cpu-execution/spec.md),
[control](specs/emulator-control/spec.md), and [console](specs/emulator-cli/spec.md) contracts for required behavior.

NESFile already parses supported cartridges; Machine connects RAM and fixed mapper-0 PRG ROM. CPU(machine) already
initializes registers through one reset, exposes register/flag properties, and supplies log_state(event). It has
seven separate booleans including the documented software B field. Preserve this implemented interface.
The reset-cpu change is archived; [cpu-reset](../../specs/cpu-reset/spec.md) records its implemented contract.
No instruction execution, host execution loop, or application entry point currently exists.

## Goals / Non-Goals

**Goals:**

- Keep opcode semantics inside CPU, address routing inside Machine, and host execution control inside Emulator.
- Give the current console and a future graphical UI the same step, bounded-run, and reset entry points.
- Use one execution path so tracing, exceptions, and future breakpoint checks have consistent instruction boundaries.
- Use accumulated CPU cycles to bound host execution and provide a shared time base for later device synchronization.

**Non-Goals:**

- Instructions outside the eight selected encodings, IRQ/NMI delivery, bus-cycle scheduling, and peripheral progression.
- Breakpoint storage or callbacks, scheduling frameworks, threads, host command registries, and pygame integration.
- ROM changes, corrupted-input handling, exception wrappers, or a new packaging/build setup.

## Decisions

### Preserve component wiring and put execution control in Emulator

Add src/emulator.py with Emulator(machine). It retains the connected Machine and constructs one CPU(machine).
Construction relies on CPU's existing startup reset and performs no additional reset or instruction. A read-only
cpu property exposes that CPU for register inspection; UI execution and reset requests go through Emulator.
Machine's constructor and byte interface remain memory-only, preserving the existing cpu-memory contract.

The component relationship is:

```text
main.py loads NESFile -> connects Machine -> constructs Emulator -> constructs CPU(machine)
main.py calls Emulator.run(cycles) -> Emulator.step() -> CPU.step() -> Machine.read_byte(address)
main.py or future UI calls Emulator.reset() -> CPU.reset() -> Machine reset-vector reads
```

Keeping the outer loop in main.py allows a later UI to alternate bounded execution with input and rendering.
An alternative is to move the loop into Machine or CPU; that would mix host control with address routing or opcode
semantics. Passing independently constructed CPU and Machine into Emulator would also require callers to keep their
connections consistent. Constructing the CPU once inside Emulator is sufficient for this first application.

### Execute the selected implied instructions in CPU.step()

Capture the original PC and consume its opcode through `_fetch_byte()`. The fetch helpers read through Machine and
advance the 16-bit PC after the requested reads succeed. `_fetch_word()` reads two consecutive bytes, low byte first,
wrapping the second address to $0000 when the first is $FFFF.

Use the opcode to index a fixed 256-entry table, with a comment naming the hexadecimal range of each group of 16
entries. Each implemented opcode has a reference to its CPU handler, starting with SEI at $78. Empty entries hold
None and trigger the existing NotImplementedError diagnostic. Pass the current CPU, original address, and fetched
opcode to the selected handler. Each handler adds its instruction's cycles and emits its own trace.

| Instruction | Opcode | Effect | Bytes | Cycles |
| --- | --- | --- | --- | --- |
| CLC | $18 | C=false | 1 | 2 |
| SEC | $38 | C=true | 1 | 2 |
| CLI | $58 | I=false | 1 | 2 |
| SEI | $78 | I=true | 1 | 2 |
| CLD | $D8 | D=false | 1 | 2 |
| SED | $F8 | D=true | 1 | 2 |
| CLV | $B8 | V=false | 1 | 2 |
| NOP | $EA | Preserve all flags | 1 | 2 |

Advance PC as (instruction_address + 1) AND $FFFF and return without fetching the next opcode. Preserve A/X/Y/SP,
the software B field, and all flags other than the selected target. Fetch no operand and perform no memory writes.
The method returns None; callers inspect CPU properties for state and accumulated cycles.

The [MOS flags chapter][mos-flags] explains the flag instructions; [NESdev's reference][nes-instructions] supplies
their encodings and cycle counts. NOP support is limited to the official $EA byte; unofficial NOP encodings still fail.
CLD and SED change the stored D flag even though NES arithmetic does not provide decimal mode. No arithmetic is added.
CLI and SEI update stored I at instruction completion. Their hardware IRQ-polling delay belongs to later IRQ support;
no IRQ/NMI delivery or bus-cycle scheduling is introduced here. The second cycle's dummy access remains omitted.

The user explicitly expanded this change to the eight encodings. Keep one implementation task per instruction,
including focused tests, to preserve the learning sequence. Test each target flag initially clear and set; otherwise
an idempotent flag assignment could hide a missing implementation. NOP must still advance PC and consume two cycles.

### Count completed instruction cycles without scheduling devices

Add private _cycles initialized to zero once during CPU construction and expose a read-only cycles property.
Use an ordinary Python integer without masking or a setter. Every completed instruction increments it by that
opcode's documented count, before reporting completion; all eight selected encodings contribute two.
A flag already holding the requested value still costs two cycles, and NOP also costs two.

Do not change cycles on a failed opcode read or unsupported opcode. Completed instructions retain their accumulated
cycles if a later step fails. Separate CPU instances own separate counters. step() and run(cycles) return None.
A step executes one instruction; run(cycles) measures its budget using the change in the same CPU.cycles counter.

Keep the counter across repeated CPU.reset() and Emulator.reset(). Constructor initialization alone starts it at zero.
Functional startup and reset add no cycles: reset is not an instruction, and its existing omitted bus activity is
outside this initial instruction-cycle counter. This is an explicit timing simplification, including omission of
hardware reset's seven cycles. Document it so later device synchronization can define reset/interrupt accounting.
The counter is a foundation for later timing; it does not advance PPU/APU, wait in real time, or model bus phases.

### Stop on missing behavior without consuming the failed opcode

If the fetched opcode has no handler, restore the original PC and raise NotImplementedError with the instruction
address and opcode in hex. A failed opcode read propagates Machine's exception before the fetch advances PC.
Both stops keep the failing address available for inspection and skip the completed-instruction trace.

This diagnostic stop policy is emulator behavior, not a claim about physical execution of unsupported opcodes.
Completed instructions in a block retain their effects; a later exception does not roll back the block.

### Format aligned instruction traces after execution

Each handler calls CPU.log_instruction(address, instruction_bytes, mnemonic, operands="") once after updating flags,
PC, and cycles. The helper formats the instruction prefix and delegates the state suffix to log_state(). Each handler
supplies its mnemonic and, for implied addressing, uses the empty operand text.

Use the exact instruction-message layout below. Column numbers are one-based:

| Field | Width | First column | Rendering |
| --- | --- | --- | --- |
| Address | 4 | 1 | Original PC as uppercase hexadecimal, zero-padded, without a prefix |
| Instruction bytes | 8 | 8 | One to three uppercase byte pairs separated by spaces, left-aligned |
| Mnemonic | 3 | 19 | Uppercase, left-aligned |
| Operands | 20 | 23 | Decoded argument text, left-aligned; blank for implied addressing |
| CPU state | Existing suffix | 44 | A/X/Y/SP/PC and symbolic P from log_state(), then CYC=<total> |

Put three spaces after the address and byte field, and one after the mnemonic and operand field. Use spaces rather
than tabs. Pad absent bytes and arguments with spaces; never display bytes that were not fetched. Ordinary operand
notation fits the reserved 20 characters, so there is no truncation, alignment configuration, or input-validation layer.

For a first SEI at $8000 after startup, the exact completed line is:

```text
8000   78         SEI                      A=00 X=00 Y=00 SP=FD PC=8001 P=--1--I-- CYC=2
```

The instruction address stays $8000 while the suffix shows the resulting PC=$8001 and cumulative CYC=2.
The address/bytes/mnemonic/operand prefix ends at column 42; column 43 is the separator, and state starts at 44.
Cycle digits grow at the end of the state suffix without shifting any earlier column.

Keep log_state(event) as the reusable state logger. Extend it with an optional separator=": " argument so existing
one-argument event calls retain their separator. The instruction helper passes separator=" " after its padded prefix,
giving the requested layout without a colon between operands and registers. Append CYC=<current cycles> after P in
the shared state suffix, including reset/helper messages. Keep their message expectations in logger-only tests.
CPU and Emulator configure no handlers or logging levels; the console uses a message-only logging format.

Pass the actual opcode byte already fetched for each current instruction. When later instructions fetch operands,
retain those bytes for their trace. Do not reread memory after execution or fetch up to three bytes just for logging:
extra reads could touch device registers, and rereading modified memory could misrepresent the executed instruction.

Formatting-only examples illustrate the reserved columns; LDA/JMP execution remains unsupported in this change:

```text
8000   78         SEI                      A=...
8001   A9 10      LDA #$10                 A=...
8003   4C 00 C0   JMP $C000                A=...
```

Keep focused logger-only cases in test/test_cpu_logging.py. Call log_instruction() and log_state() directly with known
CPU state and supplied metadata for one-, two-, and three-byte layouts; check padding, state suffixes, and that the
helpers do not change state or access memory. These cases do not execute CPU.step() or test tracing for every opcode.
Move existing reset/log_state logging-only cases into that file when updating their CYC expectations.
Instruction, facade, and CLI execution tests make no assertions about logger calls, records, counts, or trace text.
Review the post-execution logging call and captured-byte wiring in the implementation; inspect traces during manual
ROM exploration rather than adding execution tests for logging.

### Implement a small synchronous control facade

Expose the following methods, each returning None:

| Operation | Behavior |
| --- | --- |
| step() | Delegate one instruction to the existing CPU instance |
| run(cycles) | Call self.step() until the elapsed CPU cycle count reaches the requested budget |
| reset() | Delegate once to the current CPU's repeated reset |

Assume nonnegative integer cycle budgets. At entry, capture start_cycles from CPU.cycles and set the target to
start_cycles + cycles. Keep calling self.step() while CPU.cycles is below that target. This uses the actual costs
charged by CPU execution; do not estimate a number of instructions or divide the budget by the current cost of two.
A zero budget performs no step. Do not add validation, retries, exception translation, or an instruction counter.

The last step always completes, even if it crosses the target. For two-cycle instructions, run(3) consumes four cycles
and run(1) consumes two. Stop at that boundary without splitting an instruction, fetching the next opcode, or undoing
any state or cycles. A failure before the target propagates with partial progress retained.

Every call starts from the current actual counter; it does not keep a pending target or transfer overshoot to another
call. Thus two run(3) calls consume eight cycles. A prior step() or reset() does not invalidate the next budget.
The caller can read CPU.cycles before and after a block to obtain its actual duration. A future subsystem scheduler
can use that cumulative time base and account for overshoot when choosing its next budget; no scheduler is added here.

Calling self.step() instead of CPU.step() inside the loop keeps one facade boundary for future breakpoint checks.
No breakpoint registry, placeholder methods, or callback rules are introduced in this change.

The user selected reset with RAM preservation. Emulator.reset() keeps CPU, Machine, and cycles, applies CPU.reset(),
and does not reconstruct components or clear RAM. SP therefore decrements from its current value by three, and the
existing preserved-register/flag rules still apply. PPU/APU do not exist yet, so there is no additional device reset.
Reconstruction would model another power-on and lose RAM; it is a separate action, not this reset operation.

### Keep console startup in root main.py

Use argparse for one positional ROM path and ordinary --help. Resolve src imports relative to main.py, following
the existing misc/nesinfo.py approach, so an absolute script path works from another working directory.
Keep relative cartridge paths relative to the caller. Protect startup with the usual __main__ guard.

Configure console logging with format="%(message)s" before CPU creation so the startup event is visible.
Then create NESFile(path), Machine(cartridge), and Emulator(machine), in that order. Do not call reset again after
construction.
Run a simple outer loop calling emulator.run(1000), requesting 1000 CPU cycles per host block. This is a cycle budget
for yielding control, without frame scheduling, peripheral progression, or real-time pacing. A future UI can select
budgets suitable for its update loop; no CLI tuning options or error-recovery layer are added here.

Let file, configuration, and execution exceptions propagate with their normal tracebacks. The expected initial run
executes the supported entry sequence and fails at the next unsupported instruction. This is the completion boundary,
rather than an application success exit or evidence that a game runs. A pygame host can later replace this outer loop.
Keep cartridge inspection in misc/nesinfo.py unchanged and separate from application startup.

### Ground acceptance and listings in the actual ROM bytes

Read-only inspection during proposal confirmed the following entry bytes; no instruction has been executed here:

| Local file | Reset PC | First file offset | Supported entry bytes | First unsupported byte |
| --- | --- | --- | --- | --- |
| BattleCity (Japan).nes | $C070 | $0080 | $78 (SEI) | $C071: $A9 |
| Super Mario Bros. (Europe).nes | $8000 | $0010 | $78 $D8 (SEI, CLD) | $8002: $A9 |

The inspected full-file SHA-256 values are:

- BattleCity: `166ec235b062aa337045832843e2916f96f12dcf08972ad747016dbe77db761c`.
- Super Mario Bros.: `ff69421b584ce898b3d4b3ab57202900c079c45cdface84d654d0368ad796ffe`.

BattleCity's 16 KiB PRG mirrors into $C000-$FFFF; its reset address maps to PRG offset $0070 and file offset $0080.
The 32 KiB image's $8000 entry maps to PRG offset zero and file offset $0010. No trainer shifts either file offset.
Use these identities in short listings under doc/disassembly/, annotating SEI and the following CLD where present.
Explain SEI's startup interrupt mask and CLD's D-flag clearing without inferring later game algorithms.
During apply, confirm the supported entry traces and the first $A9 exception: BattleCity completes one instruction
and two cycles; the 32 KiB image completes SEI and CLD and four cycles. Record execution separately from static bytes.
Implement no $A9 or later opcode in this change. No game patch is needed or permitted.

### Verify observable behavior with synthetic programs

Extend the existing CPU tests with explicit bytes for the eight selected instructions in real mapped memory.
Use RAM writes through Machine where possible. The SEI test writes $78 at $0000 and checks that I is set from each
initial value. For ROM and $FFFF cases, construct synthetic PRG bytes before connecting the cartridge.
Check target flags initially clear/set, unrelated state preservation, NOP behavior, PC wrapping, and fetch failures.
Verify cycles starts at zero, gains two per instruction, accumulates across mixed sequences, survives reset, and
stays unchanged on failure. Check unsupported-opcode diagnostics. Instruction tests cover CPU/memory results, PC,
flags, and cycle counts without capturing logs, mocking the logger, or asserting trace emission or content.
Test log helpers independently with supplied metadata in test/test_cpu_logging.py; do not add a trace test per opcode.

Facade tests cover construction without execution, independence, one step, exact cycle budgets, zero budgets, and
nonzero entry counters. With current two-cycle instructions, test budgets 1, 2, 3, and 6, whole-instruction overshoot,
successive calls after overshoot, partial progress on failure, and reset preserving RAM and accumulated cycles.
Use real components and concise reusable synthetic cartridge setup; avoid test-only component frameworks.
Console subprocess cases cover spaced paths from another directory, --help, SEI and CLD followed by failure, and
a synthetic sequence of 501 NOPs spanning two 1000-cycle blocks, followed by $A9, to prove the loop continues without
reset. Use a reset entry of $8000: the first block completes 500 NOPs and the second reaches $A9 at $81F5.
Subprocess assertions check exit status and exception type/opcode/address, without checking instruction-log text,
line counts, or alignment. Budget and cycle totals are covered by facade/CPU state tests.
Keep subprocess tests bounded with a timeout; routine pytest cases must not require local game files.

Update doc/cpu.md, add doc/execution.md, and refresh current-state notes without adding game names outside README goals.
Record facade ownership, reset/cycle semantics, aligned traces, per-call cycle budgets, overshoot, and timing limits
in doc/decisions.md. Keep existing status-property and software B decisions intact.

## Risks / Trade-offs

- Idempotent flag state can hide a missing instruction -> Test target flags clear/set and require PC/cycle changes.
- A host block could use an absolute counter or instruction count -> Test nonzero counters and cycle boundaries.
- Whole instructions can exceed a budget -> Keep actual cycles and let future scheduling use the cumulative time base.
- The console can run indefinitely on supported bytes -> Synthetic failure terminates tests; callers control real runs.
- Functional CLI/SEI omit IRQ polling details -> Document the omission and revisit it with interrupt support.
- Instruction cycles omit reset/interrupt time -> State the counter's scope before using it for device scheduling.
- Existing reset and memory APIs must stay stable -> Verify their established suites alongside execution tests.

## Migration Plan

This adds execution APIs without replacing existing loading, inspection, memory, or reset interfaces. Implement the
CPU behavior, facade, and console in the task order, with focused checks before complete integration verification.
Rollback removes the new entry point/facade and CPU execution additions, retaining the working reset and memory path.

[mos-flags]: https://lbaeza.neocities.org/mcs6500/6500_ch03
[nes-instructions]: https://www.nesdev.org/wiki/Instruction_reference
