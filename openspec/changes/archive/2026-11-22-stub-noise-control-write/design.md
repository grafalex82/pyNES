# Design

## Context

Machine routes selected audio control writes to a dummy APU. $400C is unconnected.

## Goals / Non-Goals

Accept the selected write without implementing noise audio, envelope, or counters. Reads remain unsupported.

## Decisions

Route $400C writes to APU offset $0C and reuse ignored-write logging, preserving the device boundary.

## Risks / Trade-offs

Hardware controls noise volume, envelope, and the length counter. Ignoring writes affects games using the register.
Document this approximation and check the next observed game obstacle.
