# Design

## Context

Machine routes pulse control writes and selected audio registers to a dummy APU. $4008 is unconnected.

## Goals / Non-Goals

Accept the selected write without implementing triangle audio or counters. Reads remain unsupported.

## Decisions

Route $4008 writes to APU offset $08 and reuse its ignored-write logging, preserving the device boundary.

## Risks / Trade-offs

Hardware controls triangle length and linear counters. Ignoring writes affects games using the register. Document
this approximation and check the next observed game obstacle.
