# Design

## Context

Machine routes selected audio registers to a dummy APU. $4000 is currently unconnected.

## Goals / Non-Goals

Accept the selected write without implementing sound, envelope, or pulse generation. Reads remain unsupported.

## Decisions

Route $4000 writes to APU offset $00 and reuse its ignored-write logging. This preserves the device boundary.

## Risks / Trade-offs

Hardware changes pulse width, length-counter behavior, and volume or envelope. Ignoring writes affects all games
using the register. Document this approximation and check the next observed game obstacle.
