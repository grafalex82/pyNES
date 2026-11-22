# CPU-visible memory

[`Machine`](../src/machine.py) connects the implemented memory devices and provides byte access at NES CPU addresses.
The current implementation covers internal RAM, fixed mapper-0 PRG ROM, minimal PPU access, and dummy APU registers.
A separately constructed [`CPU`](cpu.md) uses Machine for reset and instruction accesses. Machine does not construct
the CPU, and CPU reset does not reset the full console.

## Components and address translation

[`NESFile`](../src/nesfile.py) reads a cartridge file and exposes its metadata and immutable sections through getters.
`Machine(cartridge)` takes that already parsed object, creates its own [`RAM`](../src/ram.py),
[`ROM`](../src/rom.py), [`PPU`](../src/ppu.py), and [`APU`](../src/apu.py), and uses their byte methods.
It does not reopen the cartridge file.

Machine exposes `read_byte(address)` and `write_byte(address, value)`. CPU memory and I/O requests use this interface.
Machine converts CPU addresses to device-relative offsets.
RAM and ROM know only their own storage: offset 0 means the first byte, regardless of its CPU address.

## Current memory map

All ranges below are inclusive hexadecimal CPU addresses. One KiB is 1024 bytes.

| CPU address range | Hardware role | Current behavior |
| --- | --- | --- |
| $0000-$07FF | Internal RAM | Read/write one 2048-byte buffer. |
| $0800-$1FFF | Three mirrors of internal RAM | Read/write the same buffer. |
| $2000-$3FFF | PPU video registers and their mirrors | Retain writes; status and data reads have effects. |
| $4000 | Pulse 1 control | Writes ignored; reads unsupported. |
| $4001-$4003 | Other pulse 1 registers | Not connected. |
| $4004 | Pulse 2 control | Writes ignored; reads unsupported. |
| $4005-$4007 | Other pulse 2 registers | Not connected. |
| $4008 | Triangle control | Writes ignored; reads unsupported. |
| $4009-$400B | Other triangle registers | Not connected. |
| $400C | Noise control | Writes ignored; reads unsupported. |
| $400D-$400F | Other noise registers | Not connected. |
| $4010-$4013 | DMC control, output, address, and length | Accept writes without effects; reads return $00. |
| $4014 | Sprite DMA | Write copies a CPU page into OAM without a stall; reads unsupported. |
| $4015 | APU status and channel control | Accept writes without effects; reads return $00. |
| $4016 | Controller strobe write / controller 1 read | Writes ignored; reads return $00. |
| $4017 | Controller 2 read / APU frame-counter write | Reads return $00; writes have no effects. |
| $4018-$401F | Normally disabled APU and I/O functionality | Not connected. |
| $4020-$5FFF | Cartridge expansion area | Not connected. |
| $6000-$7FFF | Cartridge RAM when present | Not connected. |
| $8000-$BFFF | PRG ROM | Read the first 16 KiB. |
| $C000-$FFFF | PRG ROM | Read the second 16 KiB, or mirror the first for a 16 KiB image. |

The hardware ranges follow the [NESdev CPU memory map][cpu-map]; the PRG layout follows [NROM][nrom].
PPU reads other than status, OAM data, or video data raise `NotImplementedError` with the device-relative offset. For example,
reading $2001 reports `PPU read at register offset 0x01 is not implemented`. Unsupported reads and writes in
$4000-$7FFF raise `NotImplementedError`, with the operation and CPU address. Controllers, expansion
hardware, and cartridge RAM have no behavior yet. No open-bus response is modeled.

## Dummy APU registers

Each Machine routes $4000/$4004/$4008/$400C writes and $4010-$4013/$4015 accesses to its APU, using offsets relative to
$4000.
Writes are accepted and logged at DEBUG without register effects. Reads of $4010-$4013 and $4015 return $00, even
after enabling DMC.
This reports all channels and IRQ flags inactive and approximates the open bus for write-only $4010-$4013 and bit 5
of $4015. It does not fetch samples, perform DMC DMA, deliver audio interrupts, or produce sound.

Writes to $4000 and $4004 are ignored without changing pulse width, volume, or envelope. Reads remain unsupported;
see [the pulse 2 control decision](decisions.md#ignored-pulse-2-control-writes-2026-11-22).

Writes to $4008 are ignored without changing triangle counters. Reads at $4008 remain unsupported; see
[the triangle control decision](decisions.md#ignored-triangle-control-writes-2026-11-22).

Writes to $400C are ignored without changing noise volume, envelope, or length counter. Reads remain unsupported; see
[the noise control decision](decisions.md#ignored-noise-control-writes-2026-11-22).

Writes at $4017 also reach the APU at offset $17 and are ignored; reads at $4017 address the controller 2 stub.
Hardware uses bit 7 to choose the frame-counter sequence and bit 6 to inhibit and clear frame IRQs.
The stub implements neither sequencing nor those IRQ effects.

The fixed response can allow a wait for DMC completion to proceed but can trap a program waiting for DMC to become
active. $4014 is sprite DMA, not a DMC register. Reads at $4014 remain unsupported. See the decisions on
[DMC/status](decisions.md#dummy-apu-register-access-2026-11-20) and
[frame-counter writes](decisions.md#dummy-apu-frame-counter-write-2026-11-20) for hardware differences and rationale.

Writes to $4016 are also ignored, without strobing either controller. Controller reads at $4016 and $4017 always
return $00; see [the controller read decision](decisions.md#fixed-controller-read-responses-2026-11-22).

## PPU register writes

Each Machine owns a PPU. Addresses $2000-$3FFF select a register offset using the low three address bits, so $2002,
$200A, and $3FFA all select offset 2. `machine.ppu.last_writes` provides an inspection tuple with the last written
byte for each offset; an unwritten offset is `None`. For example, writing $80 to $200A makes element 2 equal $80.

The $2003 and $2004 ports address and access OAM; $2006 selects a video address, and $2007 accesses video data.
Other register effects are described below.
They are accepted even at $2002, although hardware PPUSTATUS is read-only. This model also records writes immediately;
hardware ignores writes to $2000, $2001, $2005, and $2006 during an initial warmup period. See the
[decision record](decisions.md#ppu-register-write-retention-2026-11-19) for the rationale and affected ROMs.
Reads use the same offset routing. The PPU's errors for unsupported reads propagate unchanged.

## OAM access

Writing $2003 selects one of 256 OAM bytes. Writing $2004 stores a byte and advances the address modulo 256;
reading $2004 returns the selected byte without advancing. These ports also work through register mirrors.
OAM starts zero-filled, and these operations behave the same during rendering and blanking. See the
[decision record](decisions.md#functional-oam-register-access-2026-11-22) for the hardware differences.

Writing a page number to $4014 reads its 256 bytes in ascending order through the CPU memory map and writes them
through OAMDATA, starting at the selected OAM address. The address wraps and returns to its starting value after a
complete transfer. Unsupported source reads propagate their error after any preceding writes. The transfer is
synchronous and does not stall the CPU; see the [DMA decision](decisions.md#functional-oam-dma-2026-11-22).

## PPU control settings

A write to $2000 or its mirrors decodes the eight PPUCTRL bits into separate boolean settings. They start clear
and every write replaces all eight, including bits that are clear in the new value.

| Bit | Setting | Meaning when set |
| --- | --- | --- |
| 0 | `_base_nametable_x` | Select the right base nametable. |
| 1 | `_base_nametable_y` | Select the lower base nametable. |
| 2 | `_increment_32` | Advance the $2007 address by 32 instead of 1. |
| 3 | `_sprite_pattern_table_high` | Select the $1000 pattern table for 8 × 8 sprites. |
| 4 | `_background_pattern_table_high` | Select the $1000 pattern table for the background. |
| 5 | `_sprite_height_16` | Select 8 × 16 sprites instead of 8 × 8. |
| 6 | `_ext_output_enabled` | Select output on the PPU EXT pins. |
| 7 | `_nmi_enabled` | Enable vblank NMI requests. |

The address increment and NMI enable affect emulation. Nametable selection, rendering, and EXT pins are not yet
implemented by storing these settings. The retained `last_writes` inspection interface remains in place.

## PPU address writes

Two writes to $2006 or its mirrors select a video address: the first supplies the upper six bits and the second
supplies the low byte. The first write changes a temporary address only; the second copies it to the current address.
Reading $2002 or a mirror resets the write pair so the next $2006 write starts with the upper bits. Status writes do
not reset the pair. The current address and temporary address start at zero for reproducibility.

This functional model copies the address immediately after the second write and does not model sub-instruction
timing, the hardware warmup interval, or rendering-time interactions. $2005 still only retains writes and does not share
the toggle.
See [the decision record](decisions.md#ppu-address-latch-2026-11-21).

## PPU data writes

Writing to $2007 or a mirror stores a byte at the current video address. The PPU selects the increment from the
decoded bit 2 of $2000: 1 when clear or 32 when set; the initial increment is 1. Each successful write
advances the 15-bit internal address modulo $8000; PPU memory uses its low 14 bits. Normal nametable and palette
mirrors apply. A rejected CHR write propagates its error without advancing the address; the attempted register byte
is still retained for inspection.

The functional increment is applied without modeling rendering-time access restrictions or changes to the hardware's
scroll increment behavior during rendering. See [the decision record](decisions.md#ppu-data-writes-2026-11-21).

## PPU data reads

Reading $2007 or a mirror at a non-palette address returns the previous read buffer and refills it from the current
video address. The buffer starts at $00 and persists when the address is changed. At $3F00-$3FFF, the read instead
returns the six-bit palette code immediately and fills the buffer from the address $1000 lower, in $2F00-$2FFF.
The next non-palette read returns that buffered nametable byte. Successful reads advance the same 15-bit address by
1 or 32 as writes do; errors leave the address and previous buffer unchanged. CPU reset preserves the existing PPU.

Palette reads return raw six-bit codes: their upper two bits are zero instead of hardware open bus, and grayscale is
not applied. Rendering-time access effects and palette-read reliability differences between PPU revisions are not
modeled. See [the decision record](decisions.md#ppu-data-reads-2026-11-21).

## PPU status reads

Reads of $2002 and its mirrors return the current vblank flag in bit 7, with all other bits zero. Every read clears
vblank and resets the address write pair without advancing the frame phase. A second read returns $00 until a later
frame sets vblank again. The retained byte for offset 2 is separate from the returned status and is unchanged by reads.

Each new PPU starts at frame cycle 0 with vblank clear. The approximate frame lasts 29,781 nominal CPU cycles;
vblank starts at cycle 27,394 and clears at cycle 29,667 even if it was never read. `Emulator` advances the PPU after
each completed CPU instruction. CPU reset preserves the PPU and its phase. An edge of the enabled vblank condition
latches an NMI request for the execution facade. This model omits sub-instruction races, sprite status, and open bus.
See [the decision record](decisions.md#cpu-driven-ppu-vblank-2026-11-21).

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
CHR bytes are not mapped into CPU memory; the PPU accesses them in its separate video address space.

Writes at $8000-$FFFF reach `ROM.write_byte`, which raises `PermissionError` with the translated device offset.
Machine propagates that exception unchanged, leaving ROM and RAM intact. This diagnostic trap is a deliberate
departure: writes to hardware NROM do not change ROM or select banks. Bus conflicts are not modeled.
See [the ROM-write decision](decisions.md#standalone-rom-and-diagnostic-write-errors-2026-11-18) for the rationale.

## PPU pattern memory

Machine supplies a separate ROM device with the cartridge's CHR bytes to the PPU. For exactly 8192 bytes,
`machine.ppu.read_vram(address)` reads PPU addresses $0000-$1FFF in file order. The two 4 KiB pattern tables
occupy $0000-$0FFF and $1000-$1FFF. `write_vram(address, value)` routes writes to the ROM diagnostic trap and
raises `PermissionError` without changing data. This is a diagnostic departure from physical ROM behavior.

CHR RAM and CHR ROM of other sizes raise `NotImplementedError` when pattern memory is accessed. Machine construction
and CPU execution can still use a supported PRG configuration without CHR ROM. Rendering enabled background or visible
8 × 8 or 8 × 16 sprites accesses CHR ROM.
See [the CHR decision](decisions.md#fixed-chr-rom-for-the-ppu-2026-11-21).

## PPU nametable memory

Machine supplies the PPU with a separate 2 KiB RAM device for two 1 KiB nametable pages. These pages are independent
of CPU RAM and each Machine owns its own copy. New RAM starts at zero for reproducibility, not to model hardware
power-up contents. `machine.ppu.read_vram` and `write_vram` map the four logical tables as follows:

| Header mirroring | $2000 | $2400 | $2800 | $2C00 |
| --- | --- | --- | --- | --- |
| Horizontal | Page 0 | Page 0 | Page 1 | Page 1 |
| Vertical | Page 0 | Page 1 | Page 0 | Page 1 |

Addresses $3000-$3EFF mirror $2000-$2EFF; $3F00 begins the palette range. Four-screen mirroring raises
`NotImplementedError` on nametable access, while CPU execution and supported CHR access remain available.
See [the nametable decision](decisions.md#ppu-nametable-ram-2026-11-21).

## PPU palette memory

PPU addresses $3F00-$3FFF access internal palette RAM. The 32-byte range $3F00-$3F1F repeats every 32 bytes;
$3F10, $3F14, $3F18, and $3F1C also share storage with $3F00, $3F04, $3F08, and $3F0C, respectively.
Writes retain only the low six bits, and internal reads return those raw color codes. For example, a write of $E1
to $3F30 makes $3F00, $3F10, and $3F20 read as $21. Each PPU has independent zero-initialized palette storage.
Rendering uses these colors for the backdrop, stationary background, and sprites. PPUMASK bit 0 masks the displayed
color codes with $30 without changing stored palette data or the current raw PPUDATA read behavior.
See [the palette decision](decisions.md#ppu-palette-ram-2026-11-21).

## Supported configuration

Machine accepts parsed iNES or NES 2.0 cartridge data with all of the following properties:

- Mapper 0 and submapper 0.
- Exactly 16384 or 32768 PRG bytes.
- No trainer data.

Unsupported mapper, submapper, PRG-size, or trainer values raise `NotImplementedError` naming the missing support.
The loader can inspect a wider set of cartridge files than Machine can connect. Header mirroring selects supported
nametable wiring; the battery flag does not enable cartridge RAM or persistence.

CPU addresses in $0000-$FFFF and structurally valid cartridge files are assumed. RAM explicitly rejects integer write
values outside 0..255 with `ValueError` before changing storage. No address validation, corruption checks,
header repair, or exception-handling layer is added.

[cpu-map]: https://www.nesdev.org/wiki/CPU_memory_map
[nrom]: https://www.nesdev.org/wiki/NROM
[power-up]: https://www.nesdev.org/wiki/CPU_power_up_state
