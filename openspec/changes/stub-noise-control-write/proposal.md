# Proposal

## Why

Battle City stops on $400C, the next observed unimplemented write. A temporary stub permits further exploration.

## What Changes

- Route $400C writes to the dummy APU and ignore them. Leave reads unsupported.

## Capabilities

### Modified Capabilities

- `cpu-memory`: Route noise control writes to APU.
- `apu-registers`: Accept noise control writes without audio effects.

## Impact

Machine, APU, focused tests, and documentation change. No ROM is modified.
