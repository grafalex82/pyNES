# Development guide

## OpenSpec setup

OpenSpec 1.15.0 is installed on the development machine. The repository was initialized with:

```text
openspec init --tools codex --profile core --language English --no-animation
```

Codex workflow skills live in `.agents/skills/`. The installed core workflows are `openspec-explore`,
`openspec-propose`, `openspec-apply-change`, `openspec-update-change`, `openspec-sync-specs`, and
`openspec-archive-change`. The [versioned OpenSpec tool reference][openspec-tools] documents these names.

Use the exploration skill for discussion before proposing the first implementation change:

```text
$openspec-explore
Read README.md and help choose the smallest first step. Do not implement emulator code yet.
```

The setup CLI also identifies the Skills sidebar as an invocation option in the Codex desktop app.

## One small change

1. Explore the observed obstacle and explain the relevant hardware behavior.
2. Propose one instruction, one peripheral behavior, or one minimal prerequisite.
3. Read the proposal, behavior scenarios, design where useful, and tasks before implementation.
4. Implement the selected behavior with focused pytest tests and explanatory comments.
5. Run the tests and, once possible, attempt the same game again to identify the next obstacle.
6. Record the result and rationale, archive the completed change, and stop at that boundary.

For an instruction, tests should cover the selected addressing behavior, affected flags, registers, memory, and program
counter as appropriate. Several opcodes that share a mnemonic must not become an excuse to implement a large family
of instructions at once; choose the next required encoding and state its scope clearly.

When code already implements a behavior but produces the wrong result, fix that behavior rather than adding another
instruction. A bounded run is useful for detecting a polling loop that no longer makes progress.

The first game-driven loop requires a few prerequisites. Choose those individually instead of creating a broad
"bootstrap emulator" change. For example, identifying one ROM's header and mapper could be a first change; it is a
candidate to discuss, not an approved implementation plan.

## Cartridge inspection

`NESFile` and `misc/nesinfo.py` support ordinary iNES and NES 2.0 file inspection. See [usage](../README.md) and
[local ROM notes](../ROMs/README.md) for commands. Loading and inspection remain separate from emulated memory devices.

Treat cartridge inputs as structurally valid. Keep corruption checks, header repair, and exception presentation out of
this loader and utility. Unsupported declared format features remain explicit `NotImplementedError` cases.
Use synthetic files for routine tests; CLI tests also cover another working directory and paths containing spaces.

## Connected memory

`Machine` now routes CPU-addressed byte reads and writes to separate RAM and ROM components. The supported configuration
uses mapper/submapper 0, no trainer, 2 KiB of mirrored internal RAM, and fixed 16 KiB or 32 KiB PRG ROM.
The [memory guide](memory.md) explains the address map, error behavior, and deliberate hardware departures, and includes
a runnable synthetic example. The example needs no local game images and does not execute CPU instructions.

CPU register storage, status-byte conversion, and functional startup exist separately in `src/cpu.py`, using
`CPU(machine)`. Construction reads the reset vector through Machine without executing an instruction or clearing RAM.
Repeated-reset verification, reset logging, instruction execution, peripherals, bounded execution, and breakpoints
remain future work.
The memory interface lets tests and exploration scripts access bytes before those execution capabilities are added.

## Documentation roles

| Location | Content |
| --- | --- |
| `README.md` | Project goals, scope, architecture constraints, and current state |
| `AGENTS.md` | Instructions for contributors and coding assistants |
| `doc/memory.md` | Implemented memory routing, supported limits, and a synthetic byte-access example |
| `doc/cpu.md` | Register widths, boolean status fields, P conversion, and the software B convention |
| `openspec/config.yaml` | Concise context and rules for OpenSpec artifacts |
| `openspec/specs/` | Durable capability specifications maintained as changes are completed |
| `openspec/changes/` | Individually scoped proposals, designs, scenarios, and tasks |
| `doc/decisions.md` | Decisions, rationale, and documented departures from hardware |
| `doc/disassembly/` | Annotated game code and algorithm explanations |

## Questions to resolve when needed

- Confirm exact Super Mario Bros. and Battle City revisions; local hashes and header metadata are in `ROMs/README.md`.
- Clarify the eventual scope of unofficial 6502 opcodes without reducing the documented instruction-set goal.
- Define instruction/reset/interrupt behavior for the NES CPU variant as those features are introduced.
- Choose the simplest approximate PPU progression that satisfies the first observed status loop or interrupt need.
- Define the audio interface responses required by observed software, without adding audio output.
- Decide the initial bounded-execution API and breakpoint callback semantics when those capabilities are needed.

None of these questions requires a full implementation before the next small step. No mapper is selected by game name.

## Game exploration and disassembly

Keep local ROMs under `ROMs/`; the images are ignored by Git. Record their identity before using fixed addresses in
tests, explanations, or listings. Unit tests should use synthetic bytes rather than depend on these local files.

Grow listings as routines are understood. Include addresses, bytes, labels, and explanations of algorithms and device
accesses. Separate observed behavior from hypotheses; see [the listing notes](disassembly/README.md).

[openspec-tools]: https://github.com/Fission-AI/OpenSpec/blob/v1.15.0/docs/supported-tools.md
