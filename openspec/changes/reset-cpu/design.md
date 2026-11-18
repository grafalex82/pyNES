# Design

## Context

See [proposal.md](proposal.md) and [the cpu-reset spec](specs/cpu-reset/spec.md).
Machine already provides `read_byte(address)` and `write_byte(address, value)` over RAM and mapper-0 PRG ROM.
Its construction is deliberately memory-only. CPU/reset behavior is absent, while the archived memory change and
its main specification require construction without a CPU. Preserve that interface and attach CPU from the caller.

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

Use private `_a`, `_x`, `_y`, `_sp`, and `_pc` state with simple `get_<register>()` and `set_<register>(value)` methods.
Keep status in six private booleans, with get_p()/set_p() providing byte conversion as described below. Setters permit
controlled pre-reset state and later debugger use without tests reaching into private fields. Assume valid register
widths; do not add range/type checks or silent masking of ordinary A/X/Y/SP/PC inputs. Status conversion decodes and
encodes documented flag positions rather than maintaining another register value.

A separate register container or reusable processor base class would add another abstraction without a current need.
The existing getter style makes direct methods sufficient.

### Reuse one functional reset operation after initial clearing

The constructor sets A/X/Y and SP to zero and all six flag booleans to false, then calls `reset()` once. That reset
produces SP=$FD, I=1, and the vector-derived PC. Do not initialize SP to $FD before subtracting 3, which would produce
$FA on the first startup. A later `reset()` does not run constructor initialization again.

Repeated reset performs SP=(SP-3) AND $FF, sets `_interrupt_disable` to true, and reloads PC. It leaves the other
five flag variables and A/X/Y untouched, including D=true if previously set. CPU never clears or re-creates RAM.
These register effects follow the
[NES CPU power-up/reset reference](https://www.nesdev.org/wiki/CPU_power_up_state).

This separation avoids the simpler but incorrect approach of clearing all registers on every reset. A separate
power-on method is unnecessary while construction is the only initial-start path.

### Store individual flags and assemble P on demand

At the user's request, each real flag is a separate private boolean:

| Flag | Variable | P mask |
| --- | --- | --- |
| C | `_carry` | $01 |
| Z | `_zero` | $02 |
| I | `_interrupt_disable` | $04 |
| D | `_decimal` | $08 |
| V | `_overflow` | $40 |
| N | `_negative` | $80 |

`get_p()` combines the current boolean values into their documented bit positions and adds $20. Bit 4 remains clear,
so the displayed layout is NV10DIZC and initial P is $24. `set_p(value)` assigns every flag from its corresponding
input bit using boolean values, including clearing flags whose bits are 0. It ignores input bits 5 and 4.
Do not store or cache a packed P byte, and do not add B or unused-flag variables. The six booleans are the sole source
of flag state; byte conversion belongs only in get_p()/set_p(). This needs no separate flag class or per-flag API yet.

The [NES status-flag reference](https://www.nesdev.org/wiki/Status_flags) explains that bits 4 and 5 are not stored
flags and debugger representations vary. Our displayed-bit choice is a convention, not extra hardware state.
Stack serialization for PHP/BRK/interrupts will define its own B-bit behavior when those features are implemented.

### Read two vector bytes through Machine without executing anything

`reset()` reads $FFFC, then $FFFD using the existing byte method and combines low OR (high << 8) into PC.
Use explicit byte reads rather than add a general word-read helper to Machine for this one operation.
Do not cache the vector, hardcode $8000/$C070, check whether the target is mapped, or read an opcode at that target.
Existing memory exceptions propagate normally without a recovery layer.

The functional model omits the physical reset sequence's dummy reads and timing, including its stack-page reads.
The stack pointer still changes, but no stack bytes are written. Record this timing/bus simplification and the selected
initial profile in `doc/decisions.md`; no APU/PPU reset behavior or game patch is introduced.

### Log completed reset state with the standard component logger

Use `logging.getLogger("cpu")` in the CPU module. After reset completes, emit one debug event with A/X/Y/SP/PC and
`get_p()` in hexadecimal. Do not configure logging handlers or introduce a new logging-control API. The constructor's
call to reset produces one event rather than a duplicate startup event. Instruction tracing remains a later feature.

### Test state transitions against synthetic connected memory

Use `test/test_cpu.py` and synthetic NESFile/Machine configurations for both existing PRG sizes. Put asymmetric vector
bytes at their correct file offsets, seed RAM before CPU construction, and check that startup does not modify it.
Use setters to establish nonzero registers and varied flags before repeated reset, including SP values around zero.
Cover single-bit and combined P values, ignored display bits, and successive set_p() calls that clear earlier flags.
A narrow read spy can return a new vector on a later reset to prove the address is reread; never patch ROM at runtime.

Verify ordered vector reads and no writes/opcode fetch through the Machine interface. A target such as $2002 must be
loaded into PC without triggering the currently unimplemented PPU read. Use caplog to inspect reset events without
requiring a particular string layout. Existing memory/loader tests remain regression coverage; no local ROM is required.

## Risks / Trade-offs

- Initial startup and repeated reset may get conflated -> Reuse reset only after constructor-only clearing.
- SP may become negative or be reset to a constant -> Verify byte wrapping and successive decrements.
- Display bits may be mistaken for stored flags -> Document the $20 convention and keep B outside mutable state.
- A cached status byte could diverge from the flags -> Store only booleans and assemble get_p() on every call.
- Reset may fetch an opcode prematurely -> Assert only the two vector reads, including an unmapped-target case.
- Functional reset omits real bus activity -> Document the omission; exact timing remains outside project scope.

## Migration Plan

Add CPU and focused tests, then document its register interface and reset behavior in `doc/cpu.md` and the decision
record. Update relevant README, development, and memory-guide status notes without changing existing behavior or
inspection commands. No migration of persisted data, memory clearing, ROM editing, or new dependency is required.
