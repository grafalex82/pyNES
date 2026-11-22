# Proposal

## Why

Games stop at $4014 before other missing behaviors can be observed. The requested temporary stub allows execution
to continue while making the missing sprite transfer explicit.

## What Changes

- Accept and ignore writes to $4014; leave reads unsupported.
- Explain and test the omitted transfer and CPU stall. Real OAM DMA remains a separate change.

## Capabilities

### Modified Capabilities

- `cpu-memory`: Accept sprite DMA writes as a temporary no-op.

## Impact

Machine routing, focused tests, and project documentation change. No cartridge bytes change.
