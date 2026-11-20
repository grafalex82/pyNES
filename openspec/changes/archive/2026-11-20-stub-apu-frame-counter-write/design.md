# Design

## Context

See `proposal.md` for the motivation and `specs/cpu-memory/spec.md` for the routing contract. The existing dummy APU
uses the same set of supported offsets for reads and writes; Machine currently rejects both directions at $4017.

On the NES, writes to $4017 control the APU frame counter: bit 7 selects the sequencing mode and bit 6 inhibits
frame IRQs and clears a pending frame IRQ. Reads at the same address instead access controller 2.

## Goals / Non-Goals

**Goals:**

- Keep the distinction between CPU read and write routing and preserve existing dummy APU behavior.
- Explain and verify the observable limitations of discarding the frame-counter write.

**Non-Goals:**

- Implement frame sequencing, frame IRQs, controller reads, sound, or other registers.

## Decisions

- Route only writes at $4017 through Machine to the existing APU with offset $17. Leave CPU reads on the existing
  unsupported-address path. Routing both directions to APU would incorrectly hide the missing controller.
- Allow offset $17 only for APU writes, not reads, using simple direction-specific guards. Adding it to the shared
  register set would incorrectly make direct APU reads succeed.
- Ignore all written bits and retain the existing DEBUG-level ignored-write logging. Unlike hardware, this will not
  select a frame-counter mode, inhibit an IRQ, or clear a pending IRQ; $4015 continues to return inactive status.
  Simulating any part of the frame sequencer would expand this change beyond a dummy register.
- Run a bounded check with the already identified local Battle City ROM if available, stopping at the next missing
  behavior. The result is a diagnostic observation, not evidence that the game is playable.

## Risks / Trade-offs

- [Programs relying on frame interrupts or frame-clocked audio behave differently] -> Document the approximation and
  verify the stateless response without claiming hardware-accurate behavior.
- [Overlapping unarchived changes modify the same memory requirement] -> Sync or archive `add-dummy-apu-registers`
  before archiving this change; its existing requirements and scenarios are included in this delta.
