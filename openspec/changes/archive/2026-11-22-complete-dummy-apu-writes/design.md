# Design

## Context

See `proposal.md` for the motivation. Machine routes selected addresses to a stateless APU; the current read and write
sets differ, and $4017 is shared with controller 2. This change spans both modules and their CPU-visible contract.

## Goals / Non-Goals

**Goals:** Keep one simple silent register boundary and preserve the other devices sharing the address region.

**Non-Goals:** Model the bus, channel state, timing, interrupts, sound, controller behavior, or DMA timing.

## Decisions

- Route reads and writes at $4000-$4013 and $4015 to APU, and only writes at $4017. Preserve the existing DMA and
  controller paths. Separate direction-aware routing avoids treating controller 2 as an audio read.
- Accept all $4000-$4013 writes, including unused $4009 and $400D, so software can initialize the contiguous range.
  Log ignored writes through the existing APU logger. Unsupported direct APU offsets remain explicit errors.
- Return $00 for these reads without remembering writes. On hardware the channel registers are write-only and reads
  generally expose open bus; $4015 reports channel and IRQ status and has read side effects. A fixed zero continues
  the current deterministic approximation without introducing bus or timing state.
- Preserve the existing $4014 OAM page transfer and $4016/$4017 controller read behavior. Addresses $4018-$401F are
  normally disabled test functionality and remain unsupported. See [NESdev APU registers][apu] and [2A03 map][map].

[apu]: https://www.nesdev.org/wiki/APU_registers
[map]: https://www.nesdev.org/wiki/2A03

## Risks / Trade-offs

- [A game relies on channel status, interrupts, or open bus] -> Fixed $00 can produce incorrect results or polling
  loops. Document this approximation and stop at the next observed obstacle rather than claiming compatibility.
- [Existing changes overlap the same APU requirements] -> Reconcile their deltas before synchronizing or archiving.
- [DMA may read the newly supported range] -> Verify routing boundaries and retain DMA's existing transfer semantics.
