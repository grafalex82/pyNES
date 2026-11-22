# Design

## Context

The existing APU accepts selected silent writes; Machine routes only explicitly implemented addresses.

## Goals / Non-Goals

Accept only the observed $4006 write. Audio, timer state, other register writes, and open-bus reads remain outside scope.

## Decisions

Hardware writes the low eight bits of the pulse 2 timer period. The dummy discards and logs the byte, as it does for
existing audio writes. Route only $4006 through Machine; preserve unsupported reads and neighboring writes. An actual
timer alone would not provide sound and would add state without a consumer. See [NESdev pulse][pulse] and
[Mesen's pulse channel](https://github.com/SourMesen/Mesen2/blob/master/Core/NES/APU/SquareChannel.h).

[pulse]: https://www.nesdev.org/wiki/APU_Pulse

## Risks / Trade-offs

Discarding the value affects any game relying on pulse 2 sound; audio output is outside project scope. Verify this
deliberate approximation with focused tests and record the next observed obstacle without implementing it.
