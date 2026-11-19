# Execution control

## Console startup

From the repository root, pass a valid local cartridge path to the console entry point:

```text
python main.py "ROMs/your game.nes"
python main.py --help
```

Replace the example path with the file to inspect and quote paths containing spaces. From another directory, use the
absolute path to `main.py`; a relative cartridge path is resolved from the caller's working directory. The console
loads the cartridge, connects Machine, constructs Emulator once, and repeatedly requests blocks of 1000 CPU cycles.
This budget does not provide frame scheduling, peripheral progression, or real-time pacing.

The console enables DEBUG logging before CPU startup and prints message-only reset and completed-instruction traces.
Errors propagate with their ordinary traceback. For a synthetic mapper-0 ROM whose reset vector points to SEI ($78)
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
reset preserves it without adding cycles. It does not advance peripherals or represent real-time pacing or bus phases;
functional reset also omits its hardware cycles. See [the decision record](decisions.md) for the timing simplification.

`reset()` keeps the same CPU, Machine, and RAM. It reloads PC from the reset vector, subtracts three from SP modulo
256, and sets I while preserving A/X/Y, the other stored flags, and cycles. It does not execute an instruction.
The detailed CPU reset behavior is described in [the CPU guide](cpu.md).

Both single steps and bounded runs pass through the facade's `step()` boundary. This is the intended location for
future internal breakpoint checks and callbacks; breakpoint registration and callback behavior are not implemented.
