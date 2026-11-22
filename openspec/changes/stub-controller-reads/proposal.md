# Proposal

## Why

Local games now stop on controller reads. Temporary zero responses allow the next missing behavior to be observed.

## What Changes

- Return $00 from reads of $4016 and $4017 without implementing controller input.

## Capabilities

### Modified Capabilities

- `cpu-memory`: Provide fixed controller read responses.

## Impact

Machine routing, focused tests, and documentation change; no ROM is modified.
