# CPU-visible memory

[`Machine`](../src/machine.py) connects the implemented memory devices and provides byte access at NES CPU addresses.
The current implementation covers internal RAM, fixed mapper-0 PRG ROM, and inspection of PPU register writes.
A separately constructed [`CPU`](cpu.md) uses Machine for reset and instruction accesses. Machine does not construct
the CPU, and CPU reset does not reset the full console.

## Components and address translation

[`NESFile`](../src/nesfile.py) reads a cartridge file and exposes its metadata and immutable sections through getters.
`Machine(cartridge)` takes that already parsed object, creates its own [`RAM`](../src/ram.py),
[`ROM`](../src/rom.py), and [`PPU`](../src/ppu.py), and uses their byte methods. It does not reopen the cartridge file.

Machine exposes `read_byte(address)` and `write_byte(address, value)`. CPU memory and I/O requests use this interface.
Machine converts CPU addresses to device-relative offsets.
RAM and ROM know only their own storage: offset 0 means the first byte, regardless of its CPU address.

## Current memory map

All ranges below are inclusive hexadecimal CPU addresses. One KiB is 1024 bytes.

| CPU address range | Hardware role | Current behavior |
| --- | --- | --- |
| $0000-$07FF | Internal RAM | Read/write one 2048-byte buffer. |
| $0800-$1FFF | Three mirrors of internal RAM | Read/write the same buffer. |
| $2000-$3FFF | PPU video registers and their mirrors | Retain writes for inspection; reads are unimplemented. |
| $4000-$4017 | APU audio and I/O registers | Not connected. |
| $4018-$401F | Normally disabled APU and I/O functionality | Not connected. |
| $4020-$5FFF | Cartridge expansion area | Not connected. |
| $6000-$7FFF | Cartridge RAM when present | Not connected. |
| $8000-$BFFF | PRG ROM | Read the first 16 KiB. |
| $C000-$FFFF | PRG ROM | Read the second 16 KiB, or mirror the first for a 16 KiB image. |

The hardware ranges follow the [NESdev CPU memory map][cpu-map]; the PRG layout follows [NROM][nrom].
PPU reads raise `NotImplementedError` with the device-relative register offset. For example, reading $2002 reports
`PPU read at register offset 0x02 is not implemented`. Reads and writes in $4000-$7FFF raise `NotImplementedError`
with the operation and CPU address. Audio, DMA, controllers, expansion hardware, and cartridge RAM have no behavior
yet. No open-bus response is modeled.

## PPU register writes

Each Machine owns a PPU. Addresses $2000-$3FFF select a register offset using the low three address bits, so $2002,
$200A, and $3FFA all select offset 2. `machine.ppu.last_writes` provides an inspection tuple with the last written
byte for each offset; an unwritten offset is `None`. For example, writing $80 to $200A makes element 2 equal $80.

These writes only retain bytes: they do not implement rendering, interrupts, video memory, or other register effects.
They are accepted even at $2002, although hardware PPUSTATUS is read-only. This model also records writes immediately;
hardware ignores writes to $2000, $2001, $2005, and $2006 during an initial warmup period. See the
[decision record](decisions.md#ppu-register-write-retention-2026-11-19) for the rationale and affected ROMs.
Reads use the same offset routing, but PPU reads remain unimplemented; the PPU's error propagates unchanged.

## Internal RAM and its mirrors

Machine translates a RAM address with `address & 0x07FF`. Only the low eleven address bits select a byte in the
2048-byte buffer, so the four CPU windows refer to the same storage:

| Physical RAM offset | CPU aliases |
| --- | --- |
| $0000 | $0000, $0800, $1000, $1800 |
| $0123 | $0123, $0923, $1123, $1923 |
| $07FF | $07FF, $0FFF, $17FF, $1FFF |

A write through any alias is immediately visible through all four. There are no duplicate buffers to synchronize.
Each Machine owns independent RAM and starts it at zero. Zero filling is an educational convenience for reproducible
runs; real hardware has unreliable RAM contents at power-up. Machine has no reset method; `CPU.reset()` preserves
the existing RAM instead of clearing or reconstructing it.
See the [recorded departures](decisions.md#departures-and-patches) and [hardware power-up reference][power-up].

## Fixed NROM program mapping

Machine translates a PRG address with `(address - 0x8000) & (PRG byte size - 1)`.
The supported sizes are powers of two, so the mask selects an offset within the image:

| PRG size | Mask | $8000 | $BFFF | $C000 | $FFFF |
| --- | --- | --- | --- | --- | --- |
| 16 KiB | $3FFF | offset $0000 | offset $3FFF | offset $0000 | offset $3FFF |
| 32 KiB | $7FFF | offset $0000 | offset $3FFF | offset $4000 | offset $7FFF |

The 16 KiB image appears twice in the CPU window. A 32 KiB image occupies the whole window in file order.
These banks are fixed; there are no bank-selection registers or bank-switching state in this implementation.
CHR bytes remain in NESFile for later video work and are not mapped into CPU memory.

Writes at $8000-$FFFF reach `ROM.write_byte`, which raises `PermissionError` with the translated device offset.
Machine propagates that exception unchanged, leaving ROM and RAM intact. This diagnostic trap is a deliberate
departure: writes to hardware NROM do not change ROM or select banks. Bus conflicts are not modeled.
See [the ROM-write decision](decisions.md#standalone-rom-and-diagnostic-write-errors-2026-11-18) for the rationale.

## Supported configuration

Machine accepts parsed iNES or NES 2.0 cartridge data with all of the following properties:

- Mapper 0 and submapper 0.
- Exactly 16384 or 32768 PRG bytes.
- No trainer data.

Unsupported mapper, submapper, PRG-size, or trainer values raise `NotImplementedError` naming the missing support.
The loader can inspect a wider set of cartridge files than Machine can connect. Header mirroring and battery flags
remain metadata; they do not enable video behavior, cartridge RAM, or persistence.

CPU addresses in $0000-$FFFF and structurally valid cartridge files are assumed. RAM explicitly rejects integer write
values outside 0..255 with `ValueError` before changing storage. No address validation, corruption checks,
header repair, or exception-handling layer is added.

[cpu-map]: https://www.nesdev.org/wiki/CPU_memory_map
[nrom]: https://www.nesdev.org/wiki/NROM
[power-up]: https://www.nesdev.org/wiki/CPU_power_up_state
