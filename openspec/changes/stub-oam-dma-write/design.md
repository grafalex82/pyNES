# Design

## Context

Machine currently rejects $4014; the PPU has no OAM storage yet. See the proposal for the requested temporary behavior.

## Goals / Non-Goals

Allow the CPU write to finish. Implementing OAM, copying 256 bytes, and the DMA stall are outside this change.

## Decisions

Machine accepts and ignores this one write without accessing a source page. A direct routing branch keeps the temporary
behavior visible until the existing graphics roadmap implements OAM DMA. Reads still raise NotImplementedError.

## Risks / Trade-offs

Hardware transfers 256 bytes and stalls for 513 or 514 cycles. Omitting both changes sprite state and timing for all
games, so execution beyond the write does not establish playability. Record the approximation and observed stops.
