# Proposal

## Why

Battle City stops on $4008, the next observed unimplemented write. A temporary stub permits further exploration.

## What Changes

- Route $4008 writes to the dummy APU and ignore them. Leave reads unsupported.

## Capabilities

### Modified Capabilities

- `cpu-memory`: Route triangle control writes to APU.
- `apu-registers`: Accept triangle control writes without audio effects.

## Impact

Machine, APU, focused tests, and documentation change. No ROM is modified.
