# Design

## Context

Machine currently treats CPU addresses $2000-$7FFF as unconnected. See proposal.md.

## Goals / Non-Goals

Provide a separate PPU with mirrored register writes and deterministic status reads.
Rendering, timing, real vblank, NMI, open bus, and hardware register effects are out of scope.

## Decisions

Machine routes $2000-$3FFF through the low three address bits to a per-Machine PPU. The PPU retains one last
written byte per register offset for inspection, including $2002, without implementing register effects.
Expose inspection without interpreting it as a CPU register read.

Status reads return $00, then $80, alternately; all aliases share the same per-device sequence. Writes do not
advance it, and CPU.reset preserves the existing PPU. Other PPU reads remain explicitly unsupported.

This is a deliberate departure: hardware PPUSTATUS is read-only, reading it clears the vblank flag, and vblank
follows video timing. Actual PPU writes can have effects or be ignored during warmup. The chosen model allows
polling loops to progress without introducing timing. See https://www.nesdev.org/wiki/PPU_registers and
https://www.nesdev.org/wiki/PPU_power_up_state.

## Risks / Trade-offs

A read-count-driven vblank and accepted writes, including $2002, can hide hardware-dependent behavior.
Document the limitation and affected local ROMs, test it explicitly, and do not claim hardware equivalence.

## Migration Plan

Implement this PPU package first. Update existing tests and memory and CPU-execution specifications that
assume all PPU accesses are unconnected. No ROM patch or persistent-data migration is involved.
