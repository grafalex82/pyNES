# Proposal

## Why

Memory is connected, but there is no CPU state or way to obtain its starting program counter from the cartridge.
This change introduces functional CPU startup and repeated reset so the next change can execute one instruction.

## What Changes

- Add CPU register state and six separate boolean status flags, exposed as properties over private fields.
- Initialize a newly constructed CPU with the selected deterministic NES power-up register profile.
- Read the reset vector through the connected Machine and load PC without fetching or executing an opcode.
- Implement repeated reset with NES register effects, including stack-pointer wrapping and preservation of RAM.
- Assemble P when reading `p` and unpack it when assigning `p`, with no packed status state or mutable B/unused flags.
- Log completed resets with the resulting register state using the standard CPU logger.
- Test startup and repeated reset against synthetic memory and document functional simplifications.

Scope covers CPU register state and reset only. Instruction execution, dispatch tables, execution loops, IRQ/NMI
handling, stack operations, exact reset bus cycles, full-console reset, and new CLI options remain later changes.
No file checks, new dependencies, memory-device behavior, or game patches are introduced.

## Capabilities

### New Capabilities

- `cpu-reset`: Expose CPU registers, establish initial state, and perform functional reset through connected memory.

### Modified Capabilities

None. Machine construction remains memory-only; the existing `cpu-memory` and `nes-rom-loading` contracts are preserved.

## Impact

- Add `src/cpu.py` and focused tests in `test/test_cpu.py` using the existing pytest setup.
- Construct CPU from an already connected Machine and use its existing byte interface without direct device access.
- Add CPU documentation and update relevant current-state notes and decisions during implementation.
- Leave Machine, RAM, ROM, NESFile, and the inspection utility's existing public behavior intact.
- Implementation follows a separate explicit apply request after this proposal is reviewed.
