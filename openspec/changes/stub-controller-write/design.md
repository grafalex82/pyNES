# Design

## Context

Machine rejects $4016. No controller component exists; the previously selected DMA write stub is separate.

## Goals / Non-Goals

Accept the requested write without modeling controller strobe, serial input, or buttons.

## Decisions

Use a direct Machine write branch for $4016. Reads still raise NotImplementedError. This avoids introducing a
controller component before controller behavior is implemented.

## Risks / Trade-offs

Hardware writes control the strobe shared by both controllers. Ignoring them changes controller behavior in all
games; document the temporary departure and verify where local games stop.
