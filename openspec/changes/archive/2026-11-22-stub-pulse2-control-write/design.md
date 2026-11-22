# Design

## Context

Machine routes pulse 1 control writes and selected audio registers to a dummy APU. $4004 is unconnected.

## Goals / Non-Goals

Accept the selected write without implementing sound, envelope, or pulse generation. Reads remain unsupported.

## Decisions

Route $4004 writes to APU offset $04 and reuse its ignored-write logging, preserving the device boundary.

## Risks / Trade-offs

Hardware changes pulse 2 width, length-counter behavior, and volume or envelope. Ignoring writes affects all games
using the register. Document this approximation and check the next observed game obstacle.
