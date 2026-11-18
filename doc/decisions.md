# Decisions and rationale

This initial record captures the user's project constraints and the setup choices made on 2026-11-18. It does not
describe implemented emulator behavior. Add a short dated entry when a new decision is made, including the reason,
software-visible effect, and supporting references where relevant.

## Learning through one behavior at a time

Implement one instruction or one peripheral aspect per change. Once the execution path exists, the next observed
`NotImplementedError` guides the next change. This keeps each hardware concept reviewable and avoids implementing
large components before their purpose is understood. Minimal prerequisites are separate changes too.

## Machine routes CPU requests

The CPU talks to Machine rather than holding direct references to memory and peripherals. Machine selects the device
for an address and forwards the operation. This keeps CPU instruction execution independent of device implementation
and mirrors the conceptual address/data bus boundary. NES register I/O uses the memory address space.

## Functional device behavior with approximate timing

Exact device timing, video signal generation, and audio output are outside scope. Software-visible registers, memory,
interrupts, and status transitions remain part of the model. A fixed register response is insufficient if it traps a
game in a polling loop. Select and document an approximation only when the required behavior is understood.

No concrete timing model, audio response values, or game patches have been selected or implemented yet.

## NES CPU semantics

The NES CPU contains a 6502-derived core with decimal arithmetic disabled, as described by the
[NESdev 2A03 reference](https://www.nesdev.org/wiki/2A03). This distinction must be explained when arithmetic and
status instructions are introduced; ordinary MOS 6502 behavior must not be assumed where the NES differs.
The final unofficial-opcode coverage remains an exploration question.

## Simple components and standard logging

Use one Python module per component, compact classes, pygame rendering, and pytest tests. Use Python's standard
logging facility for component loggers. Instruction traces include the executed operation and the complete
post-instruction register state. Significant device events are also observable.

Single-instruction execution, bounded execution, and internal breakpoint callbacks are required capabilities to add
individually. Their APIs are not fixed by this initial setup.

## Target game identity

The target games are Super Mario Bros. and Battle City (Namco, 1985). At setup, no ROM images had been inspected.
Determine mapper requirements from the actual cartridge files and document their identities first;
[the iNES format](https://www.nesdev.org/wiki/INES) describes mapper metadata in the file header.

## OpenSpec and repository setup

Initialize the installed OpenSpec 1.15.0 with the Codex core skills and English artifacts. Record project context
without inventing a complete specification or a single large implementation change. Keep main specifications empty
at setup and evolve them through small completed changes. No emulator behavior is implemented by this setup.

Use the MIT license for original project work. Keep local ROM images, traces, caches, and environments out of Git.

## Minimal pytest setup (2026-11-18)

Keep pytest in `requirements.txt` and configure test discovery in `test/` with `src/` on the import path through
`pytest.ini`. This lets tests import component modules directly without adding packaging or build tooling.
No placeholder tests are added; focused tests will accompany the first implemented behavior.

## Ordinary cartridge file parsing (2026-11-18)

Implement `NESFile` as a filename-based class holding the original header and separate immutable trainer, PRG, and CHR
bytes. File data remains separate from future emulated memory devices; a missing CHR section does not allocate RAM.
Reading the file once and slicing its sections keeps this prerequisite small and makes offsets easy to verify.

Ordinary PRG and CHR counts use 16384-byte and 8192-byte units respectively. NES 2.0 adds the high count bits in byte 9
and extends mapper/submapper metadata in byte 8. Mirroring and battery values describe header flags only; they do not
select or implement mapper behavior. Other header fields remain available unchanged for later interpretation.

Inputs are assumed structurally valid. This step adds no signature or length validation, header repair, or game patches.
Task 2.1 is verified with synthetic files covering metadata, extended counts, optional sections, and basic flags.
The remaining unsupported-format guards and explicit rejection tests belong to task 2.2.

The field layout follows [iNES](https://www.nesdev.org/wiki/INES) and [NES 2.0](https://www.nesdev.org/wiki/NES_2.0).
[Mesen's header reader](https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesHeader.cpp) was consulted to compare
field interpretation; this parser was written independently without its compatibility heuristics or emulation features.

## Explicit unsupported cartridge features (2026-11-18)

Raise `NotImplementedError` for unknown format markers, NES 2.0 exponent-multiplier PRG/CHR sizes, nonstandard console
types, and declared miscellaneous ROM areas. These features need interpretation beyond the selected ordinary cartridge
format support. Rejecting them keeps missing behavior visible instead of silently misreading counts or dropping data.
Messages identify the unsupported feature, including the format marker, console code, or affected PRG/CHR section.

The low two bits of byte 7 declare nonstandard consoles in both supported formats. The low two bits of byte 14 declare
miscellaneous ROMs only in NES 2.0. Byte 15 is separate expansion-device metadata; a nonzero value remains preserved
in the original header without implying peripheral emulation. See the [NES 2.0 header reference][nes20-header].

These checks concern declared unsupported features. Inputs remain assumed valid, with no signature checks, length
checks, trailing-data checks, header repair, or exception handling added. Synthetic tests cover each rejection and
retain ordinary-file coverage, including a nonzero expansion-device field. No game patches or hardware approximations
are introduced.

[nes20-header]: https://www.nesdev.org/wiki/NES_2.0#Header

## NESFile getter interface (2026-11-18)

At the user's request, keep parsed values in attributes prefixed with `_` and expose them through `get_<field>()`
methods. Callers and tests use these methods for all nine metadata and section fields. A local boolean `has_trainer`
names the header flag when calculating section offsets. Parsing results and unsupported-feature errors are unchanged.

## Shared synthetic cartridge fixture (2026-11-18)

Use a local pytest fixture factory to assemble and write synthetic cartridge files in each test's temporary directory.
Tests supply explicit headers and section bytes, keeping expected values independent of the parser. This removes
duplicate file creation without introducing a second header encoder or changing the existing parsing scenarios.

## Standalone cartridge inspection and valid inputs (2026-11-18)

Keep file inspection in `misc/nesinfo.py`, using `argparse` for one positional path and `NESFile` getters for values.
Locate `src/` relative to the script so inspection works from another working directory without installation or a
configured `PYTHONPATH`. Print complete decimal mapper/submapper values, section lengths in bytes, and header flags.
This reports cartridge data without constructing devices, selecting a mapper implementation, or starting emulation.

Assume structurally valid input in both the loader and utility. Failures on damaged files are accepted, so signature,
length, section-completeness, trailing-data, and extension checks, header repair, and exception handling are excluded.
Filesystem and parsing errors propagate with ordinary Python tracebacks; corrupt-input behavior remains unspecified.
Explicit unsupported-feature guards describe missing format support rather than validating corruption.

Synthetic CLI cases verify iNES and NES 2.0 output, extended mapper/submapper fields, trainer and empty CHR sections,
header flags, paths containing spaces, execution from another working directory, and unchanged source bytes.
No hardware approximation or game patch is introduced.

## Cartridge inspection integration (2026-11-18)

Record local headers and full-file SHA-256 values in [ROM notes](../ROMs/README.md) to identify actual inputs before
selecting mapper behavior. BattleCity matches the design's NES 2.0 mapper/submapper 0, 16384-byte PRG, 8192-byte CHR,
and absent trainer. Also inspect the available Space Invaders and Super Mario Bros. files. All three CLI results match
their headers, and all three hashes are unchanged after inspection. Filenames alone do not confirm game revisions.

The full pytest suite passes 49 cases using synthetic temporary files. Local cartridge checks remain separate from
routine tests. CPU execution and mapper emulation remain later changes; no game execution is claimed.

## Initial Machine routing (2026-11-18)

Task 2.1 of `connect-memory` adds Machine, constructed from an already parsed NESFile through its getters. It owns
separate RAM and ROM devices and translates CPU addresses to device-relative byte offsets. The RAM mask `$07FF`
connects four CPU windows to one 2048-byte buffer; the PRG mask repeats a 16 KiB image or exposes all of a 32 KiB image.
Direct routing is sufficient for this fixed wiring, so no device registry or mapper framework is introduced.

The existing zero-filled RAM and diagnostic ROM-write policies also apply through Machine. ROM's PermissionError
propagates unchanged. Basic NotImplementedError paths keep unconnected addresses and unsupported configurations
explicit; focused diagnostic coverage belongs to task 2.2. Synthetic tests cover RAM aliases,
independent configurations, both PRG layouts in iNES and NES 2.0, and unchanged memory after rejected ROM writes.
The tests remove each temporary cartridge file after parsing to verify that Machine uses loaded data without rereading.
No CPU, reset, execution, hardware approximation, or game patch is added by this task.

The address wiring follows the [CPU memory map][cpu-map] and [NROM reference][nrom-map]. Mesen's
[RAM routing][mesen-ram] and [NROM bank setup][mesen-nrom] were consulted for understanding; this direct implementation
was written independently without its handler or mapper abstractions.

[cpu-map]: https://www.nesdev.org/wiki/CPU_memory_map
[nrom-map]: https://www.nesdev.org/wiki/NROM
[mesen-ram]: https://github.com/SourMesen/Mesen2/blob/master/Core/NES/InternalRamHandler.h
[mesen-nrom]: https://github.com/SourMesen/Mesen2/blob/master/Core/NES/Mappers/Nintendo/NROM.h

## Explicit Machine limits (2026-11-18)

Task 2.2 verifies the existing NotImplementedError paths without adding device behavior or input validation.
Parameterized reads and writes cover the boundaries and representative registers in the unconnected $2000-$7FFF
range, require the operation and CPU address in each diagnostic, and verify that mapped RAM and ROM remain unchanged.
Separate construction cases use complete synthetic files parsed by NESFile to check unsupported mapper bits,
submappers, PRG sizes, and trainers. Errors identify the missing configuration; successful file parsing does not imply
that Machine can emulate its cartridge hardware. No malformed files, hardware approximations, or game patches are added.

## Departures and patches

### Zero-filled standalone RAM (2026-11-18)

Task 1.1 of `connect-memory` adds a RAM component with a private bytearray and device-relative byte reads and writes.
The selected API takes a byte count and exposes only `read_byte` and `write_byte`. Both RAM and ROM take offsets
counted in bytes from the start of their own buffers: offset 0 is the first byte. CPU address translation and mirroring
belong to future Machine; the devices do not translate or mirror offsets themselves.
Valid offsets are assumed. At the user's request, `write_byte` explicitly raises ValueError for integer values outside
`0..255` before changing memory, providing a diagnostic rather than truncating the value.

Each RAM instance starts at zero to make educational runs and tests reproducible. Hardware RAM contents are unreliable
at power-up, as described by [NESdev's CPU power-up reference](https://www.nesdev.org/wiki/CPU_power_up_state).
This is a deliberate initialization convenience for future games using this component; no game has been run with it.
Focused synthetic tests verify zero initialization, all byte values and overwrites, boundary isolation, and independent
instances. CPU reset behavior remains undefined, and no game bytes are patched.

### Standalone ROM and diagnostic write errors (2026-11-18)

Task 1.2 of `connect-memory` adds ROM with private immutable bytes and the same device-relative byte methods as RAM.
The constructor receives already loaded data; file parsing and CPU address routing remain separate responsibilities.
Every `write_byte` call raises PermissionError with the device offset before changing any data, including writes of
the existing value. Synthetic tests verify source-byte reads and unchanged contents after writes at both ends and
the middle of the image. PermissionError denotes a forbidden write to this implemented device; NotImplementedError
remains reserved for unimplemented behavior.

This exception is a deliberate diagnostic departure: [NROM](https://www.nesdev.org/wiki/NROM) has fixed banks and no
mapper registers, so writes do not change its ROM or select banks. Stopping on a write makes unexpected program
behavior visible during learning. The policy will apply to games using this component; no game has been run with it,
and no ROM has been patched. Bus conflicts are not modeled. Machine routing remains future work.

For each future departure, record the expected hardware behavior, chosen behavior, reason, affected games, and
verification. For a ROM patch also record the exact ROM hash, file offset or bank/address, original bytes, replacement
bytes, and the effect on later disassembly.
