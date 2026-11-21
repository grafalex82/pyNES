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

Local cartridge metadata and file hashes are recorded in [ROM notes](ROMs/README.md).
Exact game revisions remain unconfirmed; the inspected headers declare mapper 0.

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

[`FrameDisplay`](src/frame_display.py) presents supplied 256 × 240 packed RGB frames in a 768 × 720 pygame window,
with each pixel enlarged to a 3 × 3 block. The console entry point does not yet present PPU frames automatically.

`misc\chr2png.py` provides `decode_tile(tile)` for converting one 16-byte CHR tile into an 8-by-8 grid of palette
indices. `render_chr_sheets(chr_rom, palettes, scale)` converts 8 KiB of CHR data into two off-screen pygame surfaces,
with supplied RGB palettes, one-pixel dotted separators, and 1x through 4x tile-pixel scaling. `parse_options()` parses
palette and scale arguments. The command-line utility loads a supported cartridge and writes both PNG sheets without
starting emulation.

[`NESFile`](src/nesfile.py) reads ordinary iNES and NES 2.0 metadata and extracts trainer, PRG, and CHR bytes.
Unsupported format markers, NES 2.0 exponent-multiplier sizes, nonstandard console types, and declared miscellaneous
ROM areas raise `NotImplementedError`. [`nesinfo.py`](misc/nesinfo.py) prints the format, mapper/submapper, section byte
sizes, mirroring, and nonvolatile-memory flag through `NESFile`. These values describe file metadata.

[`disassemble.py`](misc/disassemble.py) provides `load_prg_rom(path)` for mapper/submapper 0 with 16 KiB or
32 KiB PRG, `decode_prg(bytes, base)` for a linear scan, and `disassemble_prg(bytes, base)` for a two-pass listing.
Relative branches and direct `JMP`/`JSR` use labels; NMI, reset, and IRQ vector targets are named `NMI`, `START`, and
`IRQ`. Targets without a decoded line use `EQU`, and unsupported or incomplete bytes appear as `db`. A trainer is
accepted without mapping it. For 16 KiB PRG, references to the lower mirror use exact-address `EQU` aliases and each
byte is listed once at $C000-$FFFF; 32 KiB PRG is listed at $8000-$FFFF. Referenced PPU, APU, DMA, and controller
addresses use symbolic names without changing encoded addresses. Naming a register does not implement its behavior.
Linear decoding can mistake data for instructions; see [listing notes](doc/disassembly/README.md) for limitations.

[`RAM`](src/ram.py) and [`ROM`](src/rom.py) provide device-relative byte access. [`Machine`](src/machine.py) connects
zero-filled 2 KiB RAM and its CPU-address mirrors to fixed 16 KiB or 32 KiB mapper-0 PRG ROM. Construction requires
mapper/submapper 0 and no trainer. ROM writes raise `PermissionError`; unconnected addresses and unsupported cartridge
configurations raise `NotImplementedError`. See [the memory guide](doc/memory.md) for the map, supported limits,
deliberate hardware departures, and a synthetic byte-access example.

Each Machine also owns a minimal [`PPU`](src/ppu.py). Writes to $2000-$3FFF retain the last byte for each mirrored
register offset for inspection. A pair of $2006 writes selects a video address; reading $2002 resets the write pair.
Writes to $2000 decode the PPUCTRL settings; only the video address increment currently has an effect. Writes to
$2007 store video data and advance the address by 1 or 32. Status reads alternate $00 and $80 as an approximation;
other PPU register reads remain unimplemented.
Its separate video address space connects 8 KiB of mapper-0 CHR ROM at $0000-$1FFF. CHR RAM and other CHR sizes
raise `NotImplementedError` on pattern memory access. Two 1 KiB nametable RAM pages map to $2000-$3EFF using the
cartridge's horizontal or vertical mirroring; four-screen mirroring is unsupported. Palette RAM stores six-bit color
codes at $3F00-$3FFF with hardware mirrors. CPU-facing $2007 data reads remain unimplemented.
`PPU.render_frame()` produces a packed RGB frame filled with the color at $3F00, using a fixed RGB approximation.
Background and sprite layers, display masks, and the hardware's forced-blank palette override are not yet rendered.

Each Machine also owns a dummy [`APU`](src/apu.py). Writes to $4010-$4013 and $4015 have no audio effects;
reads return $00, including inactive channel and interrupt status. Writes to the APU frame counter at $4017 are also
ignored; reads at $4017 (controller 2) remain unsupported. This approximates rather than models open bus, DMC playback,
frame timing, or frame IRQs. Sprite DMA at $4014 and other unconnected registers remain unsupported.

[`CPU`](src/cpu.py) exposes `a`, `x`, `y`, `sp`, `pc`, and seven boolean status fields as read/write properties.
Reading `p` assembles NV1BDIZC; assigning it replaces all seven fields and ignores bit 5, which always reads as 1.
`break_flag` represents B in bit 4 as a software convention for inspection, rather than a physical CPU latch.
See [the CPU register guide](doc/cpu.md) for property widths, status conversion, and an example.
Construction clears register storage once, then calls `reset()` to establish A=X=Y=$00, SP=$FD, and P=$24.
PC comes from the little-endian vector at $FFFC/$FFFD through Machine. Startup preserves RAM and fetches no opcode.
Repeated reset preserves A/X/Y and N/V/B/D/Z/C, decrements SP by 3 modulo 256, sets I, and reloads the vector.
Functional reset omits dummy bus reads and timing and preserves the connected Machine and RAM.
Each completed reset calls `log_state(event)` to emit one DEBUG event through the `cpu` logger with hexadecimal
A/X/Y/SP/PC, a symbolic NV1BDIZC mask for P, and accumulated instruction cycles.
`CPU.step()` fetches and executes one instruction through Machine. Missing behavior raises `NotImplementedError`
with its byte and address. The read-only `CPU.cycles` provides a nominal total for bounded execution and does not
advance devices.
Each completed instruction emits a DEBUG trace with its address, fetched bytes, mnemonic, and resulting CPU state.
[`Emulator`](src/emulator.py) owns the connected CPU and provides single-step, cycle-budgeted run, and repeated reset
controls. Whole instructions finish even when they exceed a run budget; see [execution control](doc/execution.md).
Routine tests use synthetic files.
Local game files are kept out of version control; see [ROM notes](ROMs/README.md).

To try the frame display without a cartridge, save this example as `frame_example.py` in the repository root and run
`python frame_example.py`. It shows a synthetic RGB gradient; close its window to exit.

```python
import sys

import pygame

sys.path.insert(0, "src")
from frame_display import FrameDisplay

frame = bytes(channel for y in range(240) for x in range(256) for channel in (x, y, (x + y) % 256))
display = FrameDisplay()
pygame.display.set_caption("pyNES synthetic frame")
try:
    display.present(frame)
    while pygame.event.wait().type != pygame.QUIT:
        pass
finally:
    pygame.display.quit()
```

The frame contains RGB triples in row order, from top to bottom and left to right. The caller handles window events
and display shutdown; the presenter does not generate frames or run the emulator.

Run a supported local cartridge from the repository root:

```text
python main.py "ROMs/your game.nes"
python main.py --help
```

The console shows reset and instruction traces, then stops with a traceback at the first unimplemented behavior.
The CPU has dispatch handlers for all 151 official NES CPU opcode encodings. Unofficial opcodes and some device
behavior remain unsupported, so a ROM may still stop at a missing behavior. See
[execution control](doc/execution.md#console-startup) for the execution loop and a synthetic example.

Inspect a valid local cartridge from the repository root (replace the example path with your file):

```text
python misc/nesinfo.py "ROMs/your game.nes"
python misc/nesinfo.py --help
```

Quote paths containing spaces. From another working directory, use the full path to `misc/nesinfo.py`; a relative ROM
path is resolved from that working directory. The utility uses only the standard library and exits after inspection.
Mirroring and nonvolatile-memory values describe header flags, not effective mapper behavior.

Generate a study listing from a supported mapper-0 cartridge, without executing it:

```text
python misc\disassemble.py "ROMs\your game.nes" "listing.asm"
python misc\disassemble.py --help
```

Both paths are relative to the working directory. An existing output is overwritten, but the input cartridge cannot
be selected as the output. From another directory, use the full path to the script. The listing is not reassemblable
source or a verified disassembly; see [listing notes](doc/disassembly/README.md) for the format and limitations.

Export CHR tiles from a supported cartridge with exactly 8 KiB of CHR ROM, without executing it:

```text
python -m pip install -r requirements.txt
python misc\chr2png.py "ROMs\your game.nes" "tiles"
python misc\chr2png.py "ROMs\your game.nes" "tiles" --palette "0F 01 21 30" --scale 2
python misc\chr2png.py "ROMs\your game.nes" "tiles" --palette-file "colors.txt"
python misc\chr2png.py --help
```

Run these commands from the repository root, replacing the example paths with your own. The installed pygame must
support PNG saving; the exporter does not open a window. From another working directory, use the full script path.
ROM, palette file, and output prefix paths are relative to the working directory. Existing outputs are overwritten,
but outputs cannot identify the ROM, palette file, or each other, including through hard links.

The output prefix produces `tiles-0000.png` and `tiles-1000.png`, containing the first and second 4 KiB of CHR in
file order. Each sheet has 256 tiles in a 16-by-16 grid. `--scale` accepts integers from 1 to 4, defaulting to 1.
Each tile pixel becomes a scale-by-scale block without smoothing: scales 1, 2, 3, and 4 produce images of 143, 271,
399, and 527 pixels per side, respectively. Gray dots and transparent gaps form one-output-pixel separators at every
scale; there is no outer border.

By default both sheets use opaque black, `#555555`, `#AAAAAA`, and white for pixel values 0 through 3. `--palette`
and `--palette-file` are mutually exclusive. Either accepts exactly four or eight whitespace-separated, two-digit
hexadecimal NES color codes from `00` through `3F`, not RGB values. Four codes select colors for both sheets; eight
select four colors for each sheet, in output order. For example, a UTF-8 `colors.txt` can contain:

```text
0F 01 21 30
0F 06 16 26
```

The colors use the same fixed RGB approximation as the PPU frame renderer, not an exact video signal. CHR stores
pixel indices, not palette colors; index 0 is opaque in these sheets even for tiles used as sprites. The exporter
reads static file data without emulating mapper behavior. CHR RAM and other CHR ROM sizes are unsupported.

Cartridge inputs are assumed structurally valid. The loader and utility do not validate signatures, lengths, section
completeness, trailing bytes, or extensions, and do not repair headers or catch filesystem/parsing exceptions.
Damaged-input behavior is unspecified; ordinary Python exceptions and tracebacks are acceptable.

Install the dependencies and run pytest from the repository root:

```text
python -m pip install -r requirements.txt
python -m pytest
```

Pytest discovers tests in `test/` and adds `src/` to the import path. Routine tests do not require local game ROMs.

OpenSpec 1.15.0 was initialized for Codex using the `core` profile. Begin exploration with `openspec-explore`; the
development guide records the installed workflow names and their purpose. The implemented cartridge-file capability
is documented in [the main specification](openspec/specs/nes-rom-loading/spec.md). The completed `load-nes-rom` change
is [archived](openspec/changes/archive/2026-11-18-load-nes-rom/).

The memory capability is documented in [its main specification](openspec/specs/cpu-memory/spec.md).
The completed `connect-memory` change is [archived](openspec/changes/archive/2026-11-18-connect-memory/).

The CPU register and functional-reset capability is documented in
[its main specification](openspec/specs/cpu-reset/spec.md).
The completed `reset-cpu` change is [archived](openspec/changes/archive/2026-11-19-reset-cpu/).

## License

The emulator's original code and documentation are licensed under the [MIT License](LICENSE). Third-party materials
retain their own licenses.
