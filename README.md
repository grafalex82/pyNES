# pyNES

An educational NES emulator written in Python. The goal is to understand the console by implementing and explaining
one small piece at a time. Running games is a way to discover the next missing behavior, rather than a reason to
implement entire subsystems in advance.

## Goals

- Full instruction-level emulation of the MOS 6502-derived NES CPU, built incrementally.
- RAM, cartridge ROM, video, and controllers exposed through their software-visible addresses and registers.
- Interrupts and device behavior sufficient to execute the target games.
- Only the cartridge mappers required by the actual target ROMs.
- Annotated disassembly listings that explain the algorithms in Super Mario Bros. and Battle City (Namco, 1985).

Exact ROM revisions and mapper requirements remain to be established from the user's files.

## Out of scope

- Cycle-accurate device timing and physical signal generation, including video synchronization signals.
- Audio output. The audio subsystem should provide the register behavior and responses required by the games.
- Broad compatibility with other games or cartridge hardware before the target games require it.

Approximate timing still needs to let software make progress: status polling and interrupts cannot simply be omitted.
Any approximation or game patch must be explained in [the decision record](doc/decisions.md).

## Development approach

Attempt to run a target game, stop at the first `NotImplementedError`, and implement one instruction or one aspect of
a peripheral. Add focused pytest coverage and an explanation, then run again. Do not implement the next missing
behavior in the same change.

Before this loop can start, build the smallest ROM-loading and execution path through separate, small changes.
Unsupported behavior must remain visible instead of silently becoming a no-op or an arbitrary return value.
See [the development guide](doc/development.md) for the OpenSpec workflow and initial exploration topics.

## Architecture

`Machine` connects the components into a system. The CPU sends read and write requests to `Machine`; it never accesses
RAM, ROM, or peripheral objects directly. NES I/O is memory mapped, so device registers use the same routing path.

The CPU, RAM, ROM, controllers, video subsystem, and audio interface are separate components, with one Python module
per component. Cartridge mapping belongs to the cartridge side of the system. Introduce components only when needed.

The execution interface must eventually support both one instruction and a bounded block of instructions, so the host
can alternate between emulation, input handling, and pygame drawing. Internal breakpoints invoke Python callbacks at
selected emulated addresses, for example to enable or disable tracing within a particular routine.

Use Python's `logging` module with component loggers. Trace each executed instruction and all CPU registers after
execution. Log significant events such as mapper bank changes, video mode changes, interrupts, and controller input.
Logging controls should make detailed traces practical during game exploration.

## Tools and style

- Python for emulation, pygame for drawing, and pytest for automated tests.
- No pyenv or wheel-based project/build setup.
- English code, comments, documentation, and disassembly explanations.
- Compact code, direct classes, and no speculative abstractions or redundant checks.
- Maximum line length of 120 characters; keep a line together when it fits.
- Two blank lines between functions, including methods; one blank line between logical blocks inside a function.
- For functions with multiple logical blocks, explain each block with a one-line comment.

Use clear component boundaries and explain hardware behavior. See [AGENTS.md](AGENTS.md) for contributor instructions.

## Repository layout

| Path | Purpose |
| --- | --- |
| `doc/` | System documentation, decisions, and annotated game disassemblies |
| `src/` | Emulator components |
| `test/` | pytest tests |
| `resources/` | Graphics, firmware, and other resources when needed |
| `ROMs/` | Local game ROMs and their identification notes |
| `misc/` | Small supporting utilities |
| `openspec/` | Project context, capability specifications, and small changes |

## Current state

[`NESFile`](src/nesfile.py) reads ordinary iNES and NES 2.0 metadata and extracts trainer, PRG, and CHR bytes.
Unsupported format markers, NES 2.0 exponent-multiplier sizes, nonstandard console types, and declared miscellaneous
ROM areas raise `NotImplementedError`. [`nesinfo.py`](misc/nesinfo.py) prints the format, mapper/submapper, section byte
sizes, mirroring, and nonvolatile-memory flag through `NESFile`. These are file metadata; mapper emulation and emulator
execution are not implemented yet. Focused tests use synthetic files.
Local game files are kept out of version control; see [ROM notes](ROMs/README.md).

Inspect a valid local cartridge from the repository root (replace the example path with your file):

```text
python misc/nesinfo.py "ROMs/your game.nes"
python misc/nesinfo.py --help
```

Quote paths containing spaces. From another working directory, use the full path to `misc/nesinfo.py`; a relative ROM
path is resolved from that working directory. The utility uses only the standard library and exits after inspection.
Mirroring and nonvolatile-memory values describe header flags, not effective mapper behavior.

Cartridge inputs are assumed structurally valid. The loader and utility do not validate signatures, lengths, section
completeness, trailing bytes, or extensions, and do not repair headers or catch filesystem/parsing exceptions.
Damaged-input behavior is unspecified; ordinary Python exceptions and tracebacks are acceptable.

Install the test dependency and run pytest from the repository root:

```text
python -m pip install -r requirements.txt
python -m pytest
```

Pytest discovers tests in `test/` and adds `src/` to the import path. Routine tests do not require local game ROMs.

OpenSpec 1.15.0 was initialized for Codex using the `core` profile. Begin exploration with `openspec-explore`; the
development guide records the installed workflow names and their purpose. Main specifications remain empty until
individual capabilities have been implemented and their changes archived.

## License

The emulator's original code and documentation are licensed under the [MIT License](LICENSE). Third-party materials
retain their own licenses.
