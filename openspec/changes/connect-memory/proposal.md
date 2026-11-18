# Proposal

## Why

The loader can expose cartridge bytes, but there are no memory devices or CPU address-routing layer yet. This next
prerequisite teaches how physical RAM and PRG ROM appear at CPU addresses before CPU reset or execution is added.

## What Changes

- Add separate RAM and ROM components with byte access and private storage.
- Add Machine to connect those components and route byte reads and writes for the supported mapper-0 configuration.
- Model 2 KiB internal RAM and its CPU-address mirrors, plus the fixed 16 KiB or 32 KiB NROM program window.
- Raise PermissionError on ROM writes and propagate it through Machine without changing ROM or RAM.
- Keep unimplemented address ranges and cartridge configurations explicit.
- Start RAM at zero for deterministic educational runs and document this departure from unspecified hardware RAM state.
- Verify device operations and routing using synthetic cartridge data and existing pytest infrastructure.

Scope ends at connected CPU-visible memory. CPU construction, reset, instruction execution, video/audio/controller
registers, cartridge RAM, trainer placement, and additional mappers remain separate changes. Cartridge inspection and
the existing loader's behavior are unchanged. Valid input is assumed; no corruption checks or recovery are added.

## Capabilities

### New Capabilities

- `cpu-memory`: Provide CPU-addressed byte access to internal RAM and fixed mapper-0 PRG ROM through Machine.

### Modified Capabilities

None. The existing `nes-rom-loading` capability still describes file data and inspection without constructing devices.

## Impact

- Add `src/ram.py`, `src/rom.py`, and `src/machine.py`, following the current private-field and simple-method style.
- Consume existing NESFile getters rather than parse files again or change the inspection CLI.
- Add focused device and routing tests under `test/`; use the installed pytest setup without new dependencies.
- Explain address mirroring, supported cartridge limits, and deterministic RAM initialization in documentation.
- Keep this proposal independent of CPU reset and the next instruction-level changes.
