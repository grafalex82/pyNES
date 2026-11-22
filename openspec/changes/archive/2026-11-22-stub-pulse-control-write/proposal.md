# Proposal

## Why

Battle City stops when writing pulse-channel control at $4000. A temporary stub permits further exploration.

## What Changes

- Route $4000 writes to the dummy APU and ignore them. Leave reads unsupported.

## Capabilities

### Modified Capabilities

- `cpu-memory`: Route pulse-channel control writes to APU.
- `apu-registers`: Accept pulse-channel control writes without audio effects.

## Impact

Machine, APU, focused tests, and documentation change. No ROM is modified.
