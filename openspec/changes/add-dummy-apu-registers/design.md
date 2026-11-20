# Design

## Context

See `proposal.md` for the observed stops and selected scope. `Machine` currently raises `NotImplementedError`
for every access in $4000-$7FFF, and its tests and the `cpu-memory` specification assert that behavior. It already
owns a separate PPU and routes CPU accesses to it; the CPU accesses devices only through Machine.

## Goals / Non-Goals

**Goals:**

- Isolate the minimal audio boundary from Machine while preserving explicit errors for unrelated addresses.
- Make the consequences of the deterministic response visible and verifiable.

**Non-Goals:**

- Implement DMC sample fetching, CPU stalls, channel counters, frame timing, interrupts, or sound output.
- Implement sprite DMA, open bus, other APU registers, controllers, or a full-console reset.

## Decisions

### Route only selected addresses to a separate APU

Add a small audio component in `src/apu.py`, owned by each Machine. Machine forwards reads and writes at
$4010-$4013 and $4015, using device-relative offsets consistent with the existing component boundary. Keep $4014
on the existing unsupported path; $4014 is sprite DMA, not a DMC register.
This explicit selection avoids silently consuming accesses to unrelated devices or pretending DMA exists.

An alternative is one broad $4010-$4015 range, but it would swallow $4014 accesses and hide a missing PPU behavior.
Embedding the dummy in Machine would avoid a module but blur the existing device boundary.

### Use stateless, deterministic dummy behavior

Accept writes to the selected addresses without implementing their effects and return $00 on every selected read.
No retained write state is needed for the agreed CPU-visible behavior. Reads from $4010-$4013 do not return their
last written bytes, and writes to $4015 do not influence its status. This makes DMC appear already inactive even
immediately after a write enabling it. An alternative that sets bit 4 temporarily would invent a completion sequence
that the user did not select and might trap software in a loop without device timing.

On NES hardware $4010 controls DMC rate, looping, and IRQ enable; $4011 sets its output level; $4012 and $4013
specify the sample; and $4015 controls all audio channels on writes and reports channel and interrupt state on reads.
The dummy ignores the $4010 control bits. The $4015 DMC status bit reflects remaining sample bytes rather than simply
echoing the enable bit. $4010-$4013 are write-only; their reads
depend on open bus rather than a readable register value. Status bit 5 is also open bus. Returning zero for these
reads and all $4015 bits is therefore a documented approximation, not hardware-accurate readback.

The [cc65 NES definitions](https://github.com/cc65/cc65/blob/master/asminc/nes.inc) describe the register addresses.
The [fogleman/nes audio implementation](https://github.com/fogleman/nes/blob/master/nes/apu.go) and
[CPU routing](https://github.com/fogleman/nes/blob/master/nes/memory.go) were consulted for comparison; the dummy
will be written independently and does not copy their implementation.

### Preserve existing reset and error boundaries

CPU reset remains CPU-only and does not reconstruct or reset the APU. Unsupported accesses retain useful CPU-address
diagnostics. The existing generic unconnected-address test must stop treating $4015 as unsupported, while retaining
coverage for $4014 and adding $400F. No cartridge or ROM bytes are modified.

## Risks / Trade-offs

- [Constant inactive status can conceal meaningful channel or IRQ state] -> Document this for all connected ROMs;
  cover reads before and after writes, including enabling DMC.
- [Software waiting to see DMC become active may loop forever] -> Record this limitation; do not claim compatibility
  from register access alone. A later observed polling obstacle requires a separate change.
- [The dummy does not emulate open bus] -> State explicitly that $00 is a chosen value, not hardware readback.
- [Broad routing could hide sprite DMA or other devices] -> Test both read and write errors at $400F, $4014, and $4016.

## Migration Plan

This is a local behavioral addition with no data migration. Update the memory specification, tests, and current-state
documentation alongside the implementation; remove the new component and routing together if the change is reverted.
