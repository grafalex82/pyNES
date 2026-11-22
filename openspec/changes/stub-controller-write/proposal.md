# Proposal

## Why

The local games stop at a controller strobe write. The requested temporary stub lets execution reach the next obstacle.

## What Changes

- Accept and ignore writes to $4016; leave reads and actual controller input unsupported.

## Capabilities

### Modified Capabilities

- `cpu-memory`: Accept controller strobe writes as a temporary no-op.

## Impact

Machine routing, focused tests, and documentation change. No ROM is modified.
