# Execution control

## Console startup

From the repository root, pass a valid local cartridge path to the console entry point:

```text
python main.py "ROMs/your game.nes"
python main.py --help
```

Replace the example path with the file to inspect and quote paths containing spaces. From another directory, use the
absolute path to `main.py`; a relative cartridge path is resolved from the caller's working directory. The console
loads the cartridge, connects Machine, and constructs Emulator once. It opens a 768 × 720 window and presents the
initial PPU backdrop before requesting the first block of 1000 CPU cycles. Frame output is enabled before execution;
the PPU captures a completed frame at each vblank entry. Between blocks, the host processes window events and presents
the newest frame only when its sequence number changes. Closing the window stops execution. If multiple frames arrive
before the host checks, it presents the most recent one. This is not paced in real time. Background and sprites are
not yet rendered, so the displayed frame currently contains only the backdrop color.

The title shows presented frames per elapsed wall-clock second, refreshed between blocks after at least one second.
The initial preview counts as a presentation; captured frames skipped by the host do not. A whole interval without
presentations reports zero. The counter measures host output speed and does not control emulation speed.

The console enables DEBUG logging before CPU startup and prints message-only reset and completed-instruction traces.
Execution errors close the display and propagate with their ordinary traceback. Help does not initialize a display.
For a synthetic mapper-0 ROM whose reset vector points to SEI ($78)
at $8000 followed by unsupported $02 at $8001, SEI completes at CYC=2 and the process stops with `NotImplementedError`
identifying $02 at $8001. This is an early diagnostic stop, not a playable game.

## Host controls

`Emulator(machine)` connects host control to a supplied `Machine`. It retains that Machine and constructs one CPU,
whose startup reset reads the reset vector without executing an instruction or clearing RAM. The read-only `cpu`
property exposes the same CPU for state inspection. Machine continues to route every CPU memory access.

With an already connected `machine`, a host can control execution as follows:

```python
from emulator import Emulator

emulator = Emulator(machine)
emulator.step()       # Execute exactly one instruction.
emulator.run(3)       # Execute whole instructions until at least three more cycles have elapsed.
print(emulator.cpu.pc, emulator.cpu.cycles)
emulator.reset()      # Apply the existing repeated CPU reset.
```

`step()`, `run(cycles)`, and `reset()` return `None`. `run()` assumes a nonnegative integer budget. It measures from
the CPU cycle total at the start of each call and executes through `step()` until the budget is reached. A zero budget
does not fetch an instruction. Each instruction completes even if it crosses the target: with two-cycle instructions,
`run(3)` consumes four cycles. Two successive `run(3)` calls consume eight cycles; the first overshoot does not reduce
the second budget. Exceptions propagate, retaining completed instructions and their cycles.

`cpu.cycles` is the cumulative nominal cost of completed instructions. Construction starts it at zero, and repeated
reset preserves it without adding cycles. After each completed instruction, `Emulator.step()` advances PPU timing by
the increase in this count. A direct `CPU.step()` does not advance the PPU; failed instructions add no video progress.
The count does not represent real-time pacing or bus phases, and functional reset omits its hardware cycles.
See [the decision record](decisions.md) for the timing simplification.

`reset()` keeps the same CPU, Machine, and RAM. It reloads PC from the reset vector, subtracts three from SP modulo
256, and sets I while preserving A/X/Y, the other stored flags, cycles, and PPU state. It does not execute an
instruction.
The detailed CPU reset behavior is described in [the CPU guide](cpu.md).

Both single steps and bounded runs pass through the facade's `step()` boundary. This is the intended location for
future internal breakpoint checks and callbacks; breakpoint registration and callback behavior are not implemented.

For another host, `machine.ppu.enable_frame_output()` enables capture at subsequent vblank entries.
`machine.ppu.completed_frame` is `None` before the first capture, then holds `(sequence_number, rgb_bytes)` for the
latest frame. Each completed frame gets a new sequence number even when its pixels match the previous frame. Frame
output is disabled by default, so CPU-only callers can advance video timing without requesting rendered frames.
