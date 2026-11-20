# Decisions and rationale

This record began with the user's project constraints and setup choices on 2026-11-18; later entries describe selected
implementation decisions. Each entry reflects the project state when it was made. See [the memory guide](memory.md)
for current memory capabilities. Add a short dated entry for each new decision, including its reason,
software-visible effect, and supporting references where relevant.

### Linear instruction decoding for disassembly (2026-11-20)

Task 1.2 of `disassemble-nes-rom` adds a static decoder independent of the CPU's execution handlers. A linear scan
returns the address, original bytes, mnemonic, and operand for each official 6502 instruction. Relative branch
operands show their calculated address; labels remain later work. Unofficial opcode bytes and every byte of an
incomplete final instruction appear as `db`, preserving the entire input without claiming those bytes are code.

The [MCS6500 programming manual](https://syncopate.us/books/Synertek6502ProgrammingManual.html) describes instruction
encodings, addressing modes, and the one-byte BRK encoding. [py65's 6502 implementation][py65-6502] and an
[independent opcode reference](https://www.pastraiser.com/cpu/6502/6502_opcodes.html) were consulted for comparison;
the decoder was written independently. Synthetic tests cover all 151 official encodings, unofficial bytes, addressing
modes, relative displacements, and incomplete final instructions. This scan does not execute or modify game ROMs.

[py65-6502]: https://github.com/mnaberez/py65/blob/main/py65/devices/mpu6502.py

### Offline PRG loading for disassembly (2026-11-20)

Task 1.1 of `disassemble-nes-rom` adds `load_prg_rom(path)` to the future disassembler. It uses `NESFile` directly
and returns the original PRG bytes with a listing base of $C000 for 16 KiB or $8000 for 32 KiB. Mapper/submapper
and PRG-size limits are explicit. Unlike Machine, the offline loader accepts a trainer because `NESFile` already
separates it from PRG; this does not implement trainer mapping or execute the cartridge.

The selected windows follow the fixed PRG layout in the [memory guide](memory.md). A 16 KiB image is represented
only once; later listing work will identify its lower mirror separately. Synthetic cartridges cover both formats,
both sizes, trainers, unsupported layouts, and unchanged input. No instructions are decoded or game ROMs modified.

### Omitted indirect indexed provisional read (2026-11-19)

Indirect-indexed writes omit the hardware's provisional indexed read even when no page is crossed; indirect-indexed
loads omit it on page crossings. This keeps the functional bus model. A provisional read can trigger device side
effects; those and individual bus-cycle and DMA effects are not modeled. This applies to all ROMs and involves no
patch. Synthetic tests verify pointer wrapping and data access, not the omitted read. See section 6.5 of the
[MCS6500 programming manual](https://syncopate.us/books/Synertek6502ProgrammingManual.html).

### Omitted zero-page provisional read (2026-11-19)

Indexed-indirect and zero-page indexed accesses, including read-modify-write, omit the hardware's discarded read at
the unindexed zero-page address to retain the functional bus model. Zero-page RAM reads have no side effects here,
but bus-cycle and DMA effects are not modeled. This applies to all ROMs and involves no patch. Synthetic tests verify
address wrapping and data access, not the omitted read. See sections 6.2 and 6.4 of the
[MCS6500 programming manual](https://syncopate.us/books/Synertek6502ProgrammingManual.html).

### Omitted reads for accumulator operations (2026-11-19)

The functional model for accumulator operations omits the hardware's discarded read at the next instruction address.
This keeps bus-cycle timing outside the model, but can suppress device read side effects. The simplification applies to
all ROMs and involves no patch. Synthetic tests check the resulting register and flags, not the omitted read. See the
[MCS6500 hardware manual](https://xotmatrix.com/6502/6502-single-cycle-execution.html).

### Omitted provisional reads for indexed writes (2026-11-19)

Indexed absolute writes and read-modify-write operations omit the hardware's provisional read, retaining a functional
bus model. That read occurs even without a page crossing and may trigger device side effects; those effects, bus-cycle
timing, and DMA effects are not modeled. This applies to all ROMs and involves no patch. Synthetic tests cover effective
addresses, cycles, and read-modify-write sequences, but not the omitted read. See section 6.1 of the
[MCS6500 programming manual](https://syncopate.us/books/Synertek6502ProgrammingManual.html).

### Omitted provisional reads for indexed reads (2026-11-19)

Indexed absolute loads, comparisons, arithmetic, and logic omit the hardware's provisional read on a page crossing.
This maintains the functional bus model but skips device side effects from the provisional address and bus-cycle timing.
The simplification applies to all ROMs and involves no patch. Synthetic tests cover the results and page-crossing
cycle counts, not the omitted access. See section 6.1 of the
[MCS6500 programming manual](https://syncopate.us/books/Synertek6502ProgrammingManual.html).

### Omitted reads during subroutine return (2026-11-19)

The functional CPU omits three discarded hardware reads during subroutine return: at the next instruction byte,
the current stack location, and the saved return address. This keeps bus-cycle timing outside the model, but omits
device read side effects at the first and last addresses; DMA effects are also absent. The simplification applies to
all ROMs and involves no patch. Synthetic tests verify stack results, not the omitted accesses. See section A.5.7 of
the [MCS6500 hardware manual](https://xotmatrix.com/6502/6502-single-cycle-execution.html).

### Omitted stack-page read (2026-11-19)

During subroutine calls, the functional CPU omits the hardware's discarded stack-page read to keep bus timing outside
the model. The omitted access targets internal RAM, whose reads have no side effects in this emulator; bus-cycle and
DMA effects are not modeled. This applies to every ROM and involves no patch. Focused synthetic tests verify the
resulting stack contents, stack-pointer wrap, and operand overlap; they do not verify the omitted bus access.
See section A.5.3 of the [MCS6500 hardware manual](https://xotmatrix.com/6502/6502-single-cycle-execution.html).

### PPU register write retention (2026-11-19)

Task 1.1 of `ppu-register-writes` connects a separate PPU to each Machine. Writes to $2000-$3FFF select one of
eight offsets through the low address bits, matching the register mirrors described by the
[NESdev PPU reference](https://www.nesdev.org/wiki/PPU_programmer_reference). The last value for each offset is
retained for inspection, with `None` indicating no write. Reads remain unimplemented.

This deliberately retains all writes without register effects, including to read-only PPUSTATUS. It records writes
immediately, whereas hardware ignores writes to $2000, $2001, $2005, and $2006 during its initial warmup; see the
[NESdev power-up reference](https://www.nesdev.org/wiki/PPU_power_up_state). Retention keeps the first device boundary
inspectable without implementing the effects or timing of real PPU registers. The simplification applies to all
connected cartridges, including BattleCity (Japan), Space Invaders (J), and Super Mario Bros. (Europe) listed in
[ROM notes](../ROMs/README.md). No ROM was patched or run for these tasks. Synthetic tests cover every mirrored address,
independent Machines, status-register writes, unchanged neighboring bytes, and unsupported reads.

### Read-driven PPU status (2026-11-19)

Tasks 2.1-2.3 of `ppu-register-writes` make reads of PPUSTATUS and its mirrors alternate $00 and $80, starting at
$00 for each PPU. Reads through any alias share a sequence; writes and CPU reset do not advance or reset it. This
approximation lets a polling loop observe a clear and then a set vblank bit without implementing video timing.

On hardware, vblank follows video timing and a PPUSTATUS read clears its vblank flag and resets the scroll/address
write latch; the lower status and open-bus bits have their own meanings. See the
[NESdev PPU register reference](https://www.nesdev.org/wiki/PPU_registers). The alternating bytes do not model those
effects, rendering, or NMI and can hide timing-dependent behavior. The approximation applies to connected cartridges,
including BattleCity (Japan), Space Invaders (J), and Super Mario Bros. (Europe) in [ROM notes](../ROMs/README.md).
Synthetic tests verify aliases, independent PPUs, writes, and unsupported reads. No ROM was patched or run
for these tasks; integration checks and the next observed obstacle remain separate work.

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

## Connected memory integration (2026-11-18)

The complete pytest suite passes 133 cases: 84 memory-device and routing cases plus 49 existing loader and inspection
cases. All use synthetic data, with no dependency on local game ROMs. NESFile getters and CLI output retain their
existing contracts. The earlier synthetic documentation example also verifies both PRG layouts.

Strict OpenSpec validation for `connect-memory` passes. The change's code, tests, documentation, and planning text
stay within 120 characters per line and have no trailing whitespace. The implemented components expose construction
and byte access only; CPU reset, instruction execution, and peripheral behavior remain future work. No game execution
or game patch is introduced by this change.

## CPU register state and separate flags (2026-11-18)

Task 1.1 of `reset-cpu` adds CPU(machine) with private A/X/Y/SP/PC fields and public getter/setter methods. Register
values are assumed valid; byte registers and the 16-bit PC are assigned directly without validation or truncation.
The CPU retains the Machine reference for later memory requests. This task initializes storage to zero with all six
flags false; these defaults do not model NES power-up. Functional startup and reset remain tasks 2.1 and 2.2.

Store C/Z/I/D/V/N only as private booleans. get_p() assembles their documented positions on demand with bit 5 set and
bit 4 clear; set_p() replaces all six booleans and ignores those two display bits. No packed P, B, or unused-flag state
is retained. The displayed-byte convention keeps inspection deterministic without introducing extra hardware flags.
Synthetic tests cover register access, independent CPU states, individual and combined flag bits, ignored display
bits, and successive writes that clear earlier flags. Dedicated CPU documentation remains task 1.2.

[Mesen's status accessors](https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesCpu.h) were consulted to compare
the exclusion of bits 4 and 5 from mutable status. Its packed representation is not used here; this separate-boolean
implementation follows the selected design and was written independently. No reset, execution, or game patch is added.

## CPU register and flag properties (2026-11-18)

At the user's request, replace CPU getter/setter methods with read/write properties `a`, `x`, `y`, `sp`, `pc`, and `p`.
Expose `carry`, `zero`, `interrupt_disable`, `decimal`, `overflow`, and `negative` as boolean properties over the same
private fields. This makes test setup and assertions direct, such as `cpu.a = 0x12` and `cpu.carry = True`.
Caller-supplied register and boolean flag values are assumed valid. Reading `p` still assembles the current flags;
assigning it replaces all six flags and ignores bits 5 and 4. The earlier method-based CPU interface is superseded.
At the user's request, tests focus on flag packing/unpacking with individual bits and all-set/clear bytes.
These state-only tests construct CPU(None) without cartridge files or memory fixtures.
Startup/reset remains future work.

## CPU register range assertions (2026-11-18)

At the user's request, register setters now assert unsigned value ranges before changing state: 0..255 for
A/X/Y/SP/P and 0..65535 for PC. Use ordinary Python `assert` statements to catch invalid caller values during
development, without truncation or a shared validation framework. The P assertion precedes all flag assignments,
so a rejected value leaves every status field intact. Integer register inputs and boolean flag inputs are assumed.
Assertions are omitted with Python's `-O` option. One parameterized test checks both accepted endpoints and values
just outside each register's range, including preservation of the previous value after rejection.

## Functional CPU startup (2026-11-18)

Task 2.1 of `reset-cpu` makes construction clear register storage once and call `reset()`. Starting SP at zero lets
the reset decrement by 3 modulo 256 produce $FD. Reset sets I and reads $FFFC followed by $FFFD through Machine,
combining the bytes as low OR (high << 8). Initial A/X/Y are zero, B is false, and displayed P is $24.
The existing Machine remains memory-only; callers construct CPU after connecting the cartridge.

This selects a deterministic startup profile for educational runs. Hardware startup values should not be treated as
portable guarantees. The functional operation omits reset's dummy bus reads, including stack-page reads, and timing;
it performs no memory writes or opcode fetch. This keeps the prerequisite focused on register state and vector loading.
The simplification applies to future games using this CPU; no game has been run and no ROM has been patched.
Synthetic 16 KiB and 32 KiB cartridges verify initial registers/flags, vector order and byte order, and unchanged RAM.
Property tests now use a Machine mock for the constructor's vector reads. Repeated-reset verification and debug
logging remain later tasks, along with the complete reset documentation review.

[Mesen's reset code](https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesCpu.cpp) was consulted to compare its
initial register profile and vector loading. This implementation follows the selected constructor/reset separation
independently and does not adopt its timing or full-console reset machinery.

## Reusable CPU test setup with real memory (2026-11-18)

At the user's request, CPU tests now use a `make_cpu` factory fixture returning a real CPU and Machine backed by a
synthetic cartridge. A small iNES header function takes named PRG/CHR bank counts and mapper instead of positional
header bytes. The default reset vector points to $0000 in writable RAM, leaving test-specific data and future
instruction bytes to the test. RAM starts filled with zeros, with no test data loaded by the factory.
The `cpu` fixture accepts `prg_size` and `start_address` through pytest parametrization. The startup test checks
only CPU registers and flags. The ordered vector reads remain explicit in `CPU.reset`.
CPU behavior and instruction support are unchanged.

## Repeated CPU reset verification (2026-11-18)

Task 2.2 of `reset-cpu` verifies the existing reset operation without adding another reset path. Constructor-only
clearing remains separate: repeated calls preserve A/X/Y and N/V/B/D/Z/C, wrap SP after subtracting 3, set I, and
reload PC. B preservation is the existing software inspection convention; no new hardware departure is introduced.

Synthetic cases exercise two successive resets, clear/set preserved flags, SP around zero and at $FD, and both PRG
layouts. Moving PC away from the vector before each call checks restoration, including a $2002 target that would
raise NotImplementedError if fetched. Source review confirms fresh ordered Machine reads at $FFFC/$FFFD on every call.
Separate cases fill real RAM after construction and verify unchanged bytes, including the stack page, after both resets.
No read/write mocks, ROM changes, instruction execution, or local game files are used. Reset logging remains task 2.3.

## Completed CPU reset logging (2026-11-19)

Task 2.3 of `reset-cpu` adds the standard `cpu` component logger and one DEBUG event after the vector has loaded PC.
The event identifies reset completion and reports A/X/Y/SP/PC/P in hexadecimal, computing P from the current flags.
Keeping the event inside `reset()` gives construction one event and each later reset one event, with no duplicate
startup message. CPU configures no handlers or logging levels, leaving output control to the caller.

Six synthetic `caplog` cases cover startup and two successive resets with both PRG sizes, wrapped SP, and preserved
flags clear or set. All 51 CPU tests pass. Instruction tracing remains future work; no hardware behavior or ROM changes.

## Reusable CPU state logging with symbolic flags (2026-11-19)

At the user's request, extract `CPU.log_state(event)` from reset so another event can report the current CPU state
through the same `cpu` DEBUG logger. Reset calls it once with `Reset completed` after loading PC.
The helper appends hexadecimal A/X/Y/SP/PC and replaces numeric P in the log with eight symbols in NV1BDIZC order.
Set flags use their uppercase letters, clear flags use `-`, and bit 5 always uses `1`; P=$05 gives `--1--I-C`.
This makes individual flags directly readable while leaving the numeric `p` property and stored booleans unchanged.

Ten direct-helper cases check event text, individual flags, constant bit 5, combined masks, and unchanged CPU state.
The updated startup/repeated-reset logging cases and all other CPU tests pass: 61 synthetic cases in total.
At the user's request, logging tests compare complete messages to check register order, separators, and flag formatting.

## CPU reset integration (2026-11-19)

The complete pytest suite passes 194 synthetic cases: 61 CPU cases, 84 memory-device/routing cases, and 49 loader/CLI
cases. Existing memory and cartridge-inspection contracts remain unchanged, with no dependency on local game ROMs.
The CPU tests retain real connected memory, separate flag storage, repeated-reset RAM preservation, and complete
reset/helper log-message comparisons. No game execution is claimed.

Strict OpenSpec validation for `reset-cpu` passes. Code, tests, and related documentation stay within 120 characters
per line with no trailing whitespace. Source review confirms that CPU only reads the two vector bytes through Machine;
instruction execution, execution loops, interrupts, peripheral reset, and full-console reset remain unimplemented.

## Opcode handler table (2026-11-19)

At the user's request, CPU uses one shared 256-entry tuple indexed by opcode. Each group of 16 entries is labeled
with its hexadecimal range so a new handler can be placed at its opcode. The $78 entry holds the `_sei` function.
Entries with `None` raise `NotImplementedError` with the fetched opcode and original PC before CPU state changes.
Mesen also dispatches by indexing a handler table with the fetched byte. [Mesen opcode dispatch][mesen-dispatch].

[mesen-dispatch]: https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesCpu.cpp#L1689-L1695

## Sequential instruction fetches (2026-11-19)

`_fetch_byte()` and `_fetch_word()` use PC as the address for reads through Machine. They advance the 16-bit PC by
one or two after a successful fetch. The word helper reads the low byte first and wraps the high-byte address from
$FFFF to $0000. It commits PC after both reads so a failed second read leaves PC at the start of the word.
[Mesen's byte and word reads](https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesCpu.h#L2029-L2049).

`CPU.step()` uses the byte helper for the opcode. An empty handler entry restores the original PC so the failing
instruction remains available for inspection. The word helper is available for instructions with two-byte operands.

Task 1.9 of `execute-sei` verified this diagnostic policy with synthetic RAM programs. At the time, unsupported $A9
and unofficial NOP $1A reported their byte and address. An unconnected PPU read propagated Machine's error.
At that time, the checks also confirmed that a later failure preserved the effects of preceding instructions.
This stop is an emulator diagnostic rather than hardware behavior.

## Nominal instruction cycle counter (2026-11-19)

Task 1.10 of `execute-sei` introduced the read-only `CPU.cycles` total, initialized to zero at construction. The Python
integer has no fixed-width wrap, and separate CPU instances have independent totals.

Reset preserves the total and contributes no cycles, including the initial reset. Hardware reset takes seven cycles;
omitting them keeps this counter limited to completed instructions until reset timing is modeled. It does not advance
devices or model individual bus cycles. This simplification applies to any game using CPU; no ROM is modified.
Synthetic tests cover mixed execution, reset, failures, and wrap.

## Instruction tracing (2026-11-19)

Task 1.11 of `execute-sei` logs each completed instruction at DEBUG with its original address, fetched bytes, mnemonic,
operands, and post-instruction registers, flags, and cycle total. Fixed columns make successive traces easy to scan.
Each instruction handler logs its own mnemonic, using the fetched opcode without further memory reads.
Unsupported opcodes and failed fetches stop before the trace. Reset and direct state events also show cumulative cycles.
Initial verification covered one-, two-, and three-byte formatting without further memory reads.
The byte, mnemonic, operand, and state fields begin at columns 8, 19, 23, and 44; the original address begins at 1.
When DEBUG is disabled, instruction trace formatting is skipped. Reset events still use the shared state logger.

## Shared execution controls (2026-11-19)

Tasks 2.1-2.4 of `execute-sei` introduce `Emulator(machine)` as the host's control boundary. It retains the supplied
Machine, constructs one CPU, and exposes that CPU read-only for inspection. Startup uses CPU's existing reset once;
`step()` delegates one instruction and `reset()` applies the existing repeated reset without reconstructing either
component or clearing RAM. CPU retains ownership of instruction effects and Machine retains address routing.

`run(cycles)` calls the facade's `step()` until the increase in `CPU.cycles` reaches the nonnegative budget. A zero
budget does nothing; a final instruction may overshoot, and each later call starts from the actual current total.
Two successive three-cycle budgets therefore consume eight cycles with two-cycle instructions. Failures propagate
with completed progress retained. The total counts nominal completed-instruction cycles, survives reset, and does not
advance devices or model reset timing. This preserves the previously documented reset-cycle simplification; no ROM is
modified. Focused synthetic tests cover ownership, single steps, budgets, overshoot, failure, and repeated reset.

Routing blocks through the same `step()` gives future breakpoint checks one instruction boundary without adding a
breakpoint registry or callbacks now. See [execution control](execution.md) for the implemented API.

## Console execution loop (2026-11-19)

Tasks 3.1-3.3 of `execute-sei` add a root console entry point accepting one cartridge path. It constructs NESFile,
Machine, and Emulator once, then repeatedly requests 1000-cycle blocks. This keeps host control outside the components
and gives a future UI a place to alternate execution with its own work; the current loop neither paces nor advances
devices. Relative cartridge paths use the caller's working directory, while imports resolve relative to the script.

The console enables DEBUG logging before CPU construction and uses message-only output, making startup and instruction
state visible without component-level logging configuration. Exceptions propagate with their ordinary tracebacks.
Synthetic subprocess tests verify help, a spaced relative path, the first unsupported opcode, and continuation across
a block boundary. No cartridge bytes are modified, and reaching an unsupported opcode does not mean a game is playable.

## Console checks with target cartridges (2026-11-19)

Task 4.2 ran both identified files through `main.py`. BattleCity completed SEI at $C070 with CYC=2, then stopped on
unsupported $A9 at $C071. Super Mario Bros. completed SEI at $8000 with CYC=2 and CLD at $8001 with CYC=4, then
stopped on unsupported $A9 at $8002. These are observed entry traces, not evidence of playable games.

Each full-file SHA-256 matched [the recorded value](../ROMs/README.md#inspected-local-files-2026-11-18) before and
after execution. No ROM was patched. The next instruction remains unimplemented.

## Rejected absolute writes (2026-11-19)

An absolute store reads both address bytes before Machine attempts the write. If the device rejects it, the exception
propagates with PC already past the operand, and no completed-instruction cycles are added. This differs from an
unsupported opcode, whose PC is restored for inspection. The diagnostic ROM-write trap is documented below.
Absolute stores perform the opcode and operand reads followed by the write; they require no omitted dummy read.
See the [6502 bus-cycle reference](https://www.nesdev.org/6502_cpu.txt).

## Functional branch bus activity (2026-11-19)

Taken branches omit the hardware's extra reads, including the additional read on a page crossing. The nominal cycle
counter still includes their cost, but devices see no side effects from these reads. Interrupt polling and delivery
remain unimplemented. This applies to any ROM using branches; no ROM is patched. The functional model keeps execution
at instruction boundaries rather than modeling bus cycles. See the [NESdev instruction reference][branch-cycles].

[branch-cycles]: https://www.nesdev.org/wiki/Instruction_reference

## Departures and patches

### Implied flag instructions and official NOP (2026-11-19)

The NES keeps D visible in the status register and uses binary arithmetic regardless of its value.
[NESdev 2A03 reference](https://www.nesdev.org/wiki/2A03).

The functional model of implied instructions omits the second-cycle dummy read.
[Mesen's implied addressing and IRQ polling][mesen-implied].

The 32 KiB target image completes SEI and CLD before stopping on $A9 at $8002. The 16 KiB target stops on $A9 at
$C071 after SEI. Both images matched their recorded SHA-256 hashes before and after the checks.
[Local ROM notes](../ROMs/README.md).

### Functional CLI single step (2026-11-19)

Task 1.4 of `execute-sei` registers implied CLI ($58) in the handler table. The handler clears I, and the shared
opcode fetch advances PC by one. The focused test writes $58 at $0000 in RAM and checks I from both initial values.
[MOS programming manual, §3.2.2](https://lbaeza.neocities.org/mcs6500/6500_ch03).

The functional model omits the second-cycle dummy read and hardware IRQ polling delay so this step covers the flag
effect. IRQ delivery belongs to later interrupt support. [Mesen's implied addressing and IRQ polling][mesen-implied].

### Functional SEI single step (2026-11-19)

Task 1.1 of `execute-sei` adds `CPU.step()` with one Machine read at the current PC. Implied SEI ($78) sets I and
advances the 16-bit PC by one while preserving A/X/Y/SP, the other flags, and memory. An unsupported opcode raises
`NotImplementedError` with its byte and address, leaving PC at the failed instruction for inspection.
[MOS programming manual, §3.2.1][mos-sei] and [Mesen's SEI handler][mesen-sei].

The functional step omits the hardware's second-cycle dummy read at the next address and IRQ polling delay to focus
on the register effects. The initial synthetic test confirmed that SEI at $1FFF reached $2000 without a PPU read.
[Mesen's implied addressing and IRQ polling][mesen-implied].

At the user's request, the dedicated SEI test now writes $78 to RAM at $0000 and checks I from both initial values.

Read-only checks on both target ROMs completed one SEI each. The 16 KiB image stopped at $C071 on $A9 and the 32 KiB
image stopped at $8001 on $D8. Both images matched their recorded SHA-256 hashes before and after the checks.
[Local ROM notes](../ROMs/README.md).

[mos-sei]: https://lbaeza.neocities.org/mcs6500/6500_ch03
[mesen-sei]: https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesCpu.h
[mesen-implied]: https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesCpu.cpp

### Functional CPU reset and software B preservation (2026-11-19)

Task 2.4 of `reset-cpu` records the implemented model. Six hardware flags and the additional software B field are
separate booleans; `p` assembles NV1BDIZC on demand, with no retained packed byte or bit-5 variable. Construction
clears storage once and calls reset, producing A=X=Y=$00, SP=$FD, I=1, N/V/B/D/Z/C=0, P=$24, and vector-derived PC.
This deterministic initial profile makes educational runs reproducible rather than promising portable hardware
startup values; see the [NESdev power-up reference](https://www.nesdev.org/wiki/CPU_power_up_state).

Hardware has no stored B latch; see the [status reference](https://www.nesdev.org/wiki/Status_flags#The_B_flag).
Initializing B to false and preserving it across repeated reset are deliberate software conventions for inspection.
For example, assigning P=$10 yields displayed P=$30; reset retains B, sets I, and produces P=$34.
Future stack instructions and interrupts must form their saved status independently of this inspection field.
The convention applies to future games using CPU; none has been executed with it, and no ROM patch is involved.

Hardware reset performs stack-page reads in place of pushes. The functional model omits those and other dummy reads
and reset timing, while retaining SP=(SP-3) AND $FF, I=1, and ordered vector reads through Machine at $FFFC/$FFFD.
This keeps the prerequisite focused on visible register state. A/X/Y and N/V/B/D/Z/C survive repeated reset, as does
all RAM; no stack bytes are written and no opcode is fetched. Machine construction remains memory-only, and CPU
reset neither reconstructs the system nor resets peripherals. Exact bus activity and full-console reset are absent.
Synthetic startup, repeated-reset, status-conversion, and logging cases verify the implemented effects without games.

### Stored B for status inspection (2026-11-18)

The revised task 1.1 of `reset-cpu` adds a private `_break_flag` boolean and its read/write `break_flag` property.
Reading `p` packs B into bit 4; assigning `p` replaces B from that bit along with the six hardware flags.
Only bit 5 remains a constant with no stored variable. B starts false, and no packed P byte is retained.

The [NESdev status reference](https://www.nesdev.org/wiki/Status_flags#The_B_flag) describes B as a transient signal
used when saving status, rather than a physical latch. Keeping B as mutable software state is a deliberate departure
selected for convenient inspection and byte conversion. It has no independent execution or interrupt effect.
Future stack instructions and interrupts must define their hardware behavior separately from this inspection field.
The planned repeated-reset behavior preserves B; reset itself is not implemented by this task.

The existing two conversion tests now include B=$10, packed P=$30 for B alone, all-set P=$FF, ignored input bit 5,
and replacement of previously set flags. No game has been run with this convention, and no ROM bytes are patched.

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
