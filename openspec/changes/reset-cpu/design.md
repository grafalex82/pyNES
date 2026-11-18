# Design

## Context

See [proposal.md](proposal.md) and [the cpu-reset spec](specs/cpu-reset/spec.md).
Machine already provides `read_byte(address)` and `write_byte(address, value)` over RAM and mapper-0 PRG ROM.
Its construction is deliberately memory-only. CPU register storage exists, while functional reset remains absent.
The archived memory change and its main specification require construction without a CPU. Preserve that interface
and attach CPU from the caller.

The user selected both initial CPU state and repeated reset with NES behavior. Local vector bytes were inspected
without executing code: one 16 KiB image points to $C070; the other 16 KiB image and the 32 KiB image point to $8000.
These observations help check the existing memory layout; automated tests will use synthetic cartridges instead.

## Goals / Non-Goals

**Goals:**

- Keep CPU state in one component, using Machine for all externally visible memory reads.
- Separate initial register clearing from repeated-reset effects.
- Make flags, stack-pointer wrapping, and little-endian vector loading understandable and observable.

**Non-Goals:**

- A CPU owned or automatically constructed by Machine, full-console reset, or an emulator startup command.
- Instruction dispatch, `step` stubs, execution loops, interrupts, stack pushes, and exact bus-cycle accounting.
- Register-validation frameworks, copied ROM data, exception wrappers, and new dependencies.

## Decisions

### Construct CPU after the existing memory configuration

Add CPU in `src/cpu.py` with `CPU(machine)`. Store only a reference to the connected Machine for memory access.
Do not import or reach into RAM, ROM, NESFile, or Machine's private storage. Machine already has the complete supported
PRG mapping, so CPU needs no cartridge-size or mapper knowledge. This keeps both existing main specs unchanged.

Use private `_a`, `_x`, `_y`, `_sp`, and `_pc` state with read/write properties `a`, `x`, `y`, `sp`, and `pc`.
Keep status in seven private booleans, exposed through matching flag properties. The computed `p` property provides
byte conversion as described below. Property assignment permits controlled pre-reset state and later debugger use
without tests reaching into private fields. Register inputs are integers and flag inputs are booleans.
At the user's request, use ordinary `assert 0 <= value <= 0xFF` in A/X/Y/SP/P setters and `$FFFF` as the PC limit.
Check P before changing any flags. This leaves prior state intact on AssertionError and omits the checks under `-O`.
Use no shared validator, type checks, or silent masking. Status conversion decodes and encodes documented flag
positions rather than maintaining another register value.

A separate register container or reusable processor base class would add another abstraction without a current need.
At the user's request, properties allow direct register and flag access in tests without a separate method API.

### Reuse one functional reset operation after initial clearing

The constructor sets A/X/Y and SP to zero and all seven flag booleans to false, then calls `reset()` once. That reset
produces SP=$FD, I=1, and the vector-derived PC. Do not initialize SP to $FD before subtracting 3, which would produce
$FA on the first startup. A later `reset()` does not run constructor initialization again.

Repeated reset performs SP=(SP-3) AND $FF, sets `_interrupt_disable` to true, and reloads PC. It leaves the other
six flag variables and A/X/Y untouched, including D=true and B=true if previously set. B preservation is a software
convention for the additional inspection field, which has no physical latch. CPU never clears or re-creates RAM.
The hardware register effects follow the
[NES CPU power-up/reset reference](https://www.nesdev.org/wiki/CPU_power_up_state).

This separation avoids the simpler but incorrect approach of clearing all registers on every reset. A separate
power-on method is unnecessary while construction is the only initial-start path.

### Store individual flags and assemble P on demand

At the user's request, keep six hardware flags and the additional software B field as separate private booleans:

| Flag | Variable | Property | P mask |
| --- | --- | --- | --- |
| C | `_carry` | `carry` | $01 |
| Z | `_zero` | `zero` | $02 |
| I | `_interrupt_disable` | `interrupt_disable` | $04 |
| D | `_decimal` | `decimal` | $08 |
| B | `_break_flag` | `break_flag` | $10 |
| V | `_overflow` | `overflow` | $40 |
| N | `_negative` | `negative` | $80 |

Reading `p` combines the current boolean values into their documented bit positions and adds $20. Bit 4 reflects
`break_flag`, so the displayed layout is NV1BDIZC. Initial B is false and initial P remains $24. Assigning `p` sets
every flag from its corresponding input bit, including clearing flags whose bits are 0; only input bit 5 is ignored.
Do not store or cache a packed P byte or add an unused-bit variable. The seven booleans are the sole source of status
state; byte conversion belongs only in `p`. Each flag property directly reads/writes its boolean.
No separate flag class is needed, and the property is named `break_flag` because `break` is a Python keyword.

### Treat stored B as a deliberate software convention

The [NES status-flag reference](https://www.nesdev.org/wiki/Status_flags#The_B_flag) explains that B is a transient
signal rather than a physical status latch. Hardware forms bit 4 when saving status: PHP/BRK push 1, IRQ/NMI push 0,
and PLP/RTI do not restore a stored B latch. Mesen's
[status accessors and PHP implementation](https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesCpu.h) keep that
distinction by excluding B from stored status and adding it for PHP.

For this educational state interface, retaining a mutable B makes bit 4 directly inspectable and supports byte
packing/unpacking through the same properties as other flags. This is a selected departure from physical state:
initialize B to false, preserve it on repeated reset, and give it no independent execution or interrupt effect.
Record this convention and its rationale in `doc/decisions.md` when implementing it. It applies to the CPU model;
no game has been run with it, and no ROM patch is proposed.
Future PHP/BRK/IRQ/NMI and PLP/RTI changes must define their hardware-correct stack behavior separately from this
inspection field. Those instructions and interrupts remain outside this change.

### Read two vector bytes through Machine without executing anything

`reset()` reads $FFFC, then $FFFD using the existing byte method and combines low OR (high << 8) into PC.
Use explicit byte reads rather than add a general word-read helper to Machine for this one operation.
Do not cache the vector, hardcode $8000/$C070, check whether the target is mapped, or read an opcode at that target.
Existing memory exceptions propagate normally without a recovery layer.

The functional model omits the physical reset sequence's dummy reads and timing, including its stack-page reads.
The stack pointer still changes, but no stack bytes are written. Record this timing/bus simplification and the selected
initial profile in `doc/decisions.md`; no APU/PPU reset behavior or game patch is introduced.

### Log completed reset state with the standard component logger

Use `logging.getLogger("cpu")` in the CPU module. A `log_state(event)` method accepts event text and appends current
A/X/Y/SP/PC in hexadecimal and P as eight symbols in NV1BDIZC order. Each clear flag appears as `-`, each set flag
uses its uppercase letter, and bit 5 always appears as `1`; P=$05 therefore appears as `--1--I-C`.
Compute the mask from the current `p` property without retaining another status representation.

After reset completes, call `log_state("Reset completed")` once. The helper only observes current state and can be
called with another event string without resetting or executing the CPU. Do not configure logging handlers or add
logging controls. The constructor's reset produces one event rather than a duplicate startup event.
Instruction tracing remains a later feature.

### Test state transitions against synthetic connected memory

Use `test/test_cpu.py` and synthetic NESFile/Machine configurations for both existing PRG sizes. Put asymmetric vector
bytes at their correct file offsets, seed RAM before CPU construction, and check that startup does not modify it.
Assign properties to establish nonzero registers and varied flags before repeated reset, including SP around zero.
For the state interface, keep two focused tests: packing flags into P and unpacking P into flags.
Extend these same two tests to cover B=$10, P=$30 with only B set, and all-set P=$FF; repeated P assignment clears B
alongside the six hardware flags. Verify that bit 5 remains the only ignored input bit.
One additional parameterized test covers accepted endpoints and rejected values immediately outside every register
range, checking that rejection preserves the previous value.
A narrow read spy can return a new vector on a later reset to prove the address is reread; never patch ROM at runtime.

Verify ordered vector reads and no writes/opcode fetch through the Machine interface. A target such as $2002 must be
loaded into PC without triggering the currently unimplemented PPU read. Use caplog to compare complete reset/helper
messages, including register order, separators, and flag masks. Existing memory/loader tests remain regression coverage;
no local ROM is required.

## Risks / Trade-offs

- Initial startup and repeated reset may get conflated -> Reuse reset only after constructor-only clearing.
- SP may become negative or be reset to a constant -> Verify byte wrapping and successive decrements.
- Stored B may be mistaken for hardware state -> Explain its software-only role and separate future stack behavior.
- A cached status byte could diverge from the flags -> Store only booleans and assemble `p` on every read.
- Reset may fetch an opcode prematurely -> Assert only the two vector reads, including an unmapped-target case.
- Functional reset omits real bus activity -> Document the omission; exact timing remains outside project scope.

## Migration Plan

Add CPU and focused tests, then document its register interface and reset behavior in `doc/cpu.md` and the decision
record. Update relevant README, development, and memory-guide status notes without changing existing behavior or
inspection commands. No migration of persisted data, memory clearing, ROM editing, or new dependency is required.

Task 1.1 implements the seven-field state interface, including software B, and its two conversion tests.
Current-state documentation describes this interface and constructor-only storage initialization.
Functional startup and repeated reset remain pending tasks.
