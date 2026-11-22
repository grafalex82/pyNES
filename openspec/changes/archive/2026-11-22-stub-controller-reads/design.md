# Design

## Context

The existing controller write stub does not implement strobe or controller hardware. $4017 writes address the APU.

## Goals / Non-Goals

Return zero from both controller reads without implementing buttons, serial state, or open bus.

## Decisions

Machine returns $00 for each controller read and retains the existing $4017 APU write routing. This follows the
temporary stub approach without introducing a controller component before its behavior is implemented.

## Risks / Trade-offs

Real controller reads expose serial data and open bus, and standard controllers return one after eight bits. Fixed
zero can change program behavior or trap waits for input; document the approximation and observed game stops.
