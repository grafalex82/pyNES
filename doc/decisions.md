# Decisions and rationale

This initial record captures the user's project constraints and the setup choices made on 2026-11-18. It does not
describe implemented emulator behavior. Add a short dated entry when a new decision is made, including the reason,
software-visible effect, and supporting references where relevant.

## Learning through one behavior at a time

Implement one instruction or one peripheral aspect per change. Once the execution path exists, the next observed
`NotImplementedError` guides the next change. This keeps each hardware concept reviewable and avoids implementing
large components before their purpose is understood. Minimal prerequisites are separate changes too.

## Machine routes CPU requests

The CPU talks to Machine rather than holding direct references to memory and peripherals. Machine selects the device
for an address and forwards the operation. This keeps CPU instruction execution independent of device implementation
and mirrors the conceptual address/data bus boundary. NES register I/O uses the memory address space.

## Functional device behavior with approximate timing

Exact device timing, video signal generation, and audio output are outside scope. Software-visible registers, memory,
interrupts, and status transitions remain part of the model. A fixed register response is insufficient if it traps a
game in a polling loop. Select and document an approximation only when the required behavior is understood.

No concrete timing model, audio response values, or game patches have been selected or implemented yet.

## NES CPU semantics

The NES CPU contains a 6502-derived core with decimal arithmetic disabled, as described by the
[NESdev 2A03 reference](https://www.nesdev.org/wiki/2A03). This distinction must be explained when arithmetic and
status instructions are introduced; ordinary MOS 6502 behavior must not be assumed where the NES differs.
The final unofficial-opcode coverage remains an exploration question.

## Simple components and standard logging

Use one Python module per component, compact classes, pygame rendering, and pytest tests. Use Python's standard
logging facility for component loggers. Instruction traces include the executed operation and the complete
post-instruction register state. Significant device events are also observable.

Single-instruction execution, bounded execution, and internal breakpoint callbacks are required capabilities to add
individually. Their APIs are not fixed by this initial setup.

## Target game identity

The target games are Super Mario Bros. and Battle City (Namco, 1985). No ROM images have been inspected. Determine
mapper requirements from the actual cartridge files and document their identities first;
[the iNES format](https://www.nesdev.org/wiki/INES) describes mapper metadata in the file header.

## OpenSpec and repository setup

Initialize the installed OpenSpec 1.15.0 with the Codex core skills and English artifacts. Record project context
without inventing a complete specification or a single large implementation change. Keep main specifications empty
at setup and evolve them through small completed changes. No emulator behavior is implemented by this setup.

Use the MIT license for original project work. Keep local ROM images, traces, caches, and environments out of Git.

## Minimal pytest setup (2026-11-18)

Keep pytest in `requirements.txt` and configure test discovery in `test/` with `src/` on the import path through
`pytest.ini`. This lets tests import component modules directly without adding packaging or build tooling.
No placeholder tests are added; focused tests will accompany the first implemented behavior.

## Departures and patches

There are no implemented departures or game patches yet. For each future departure, record the expected hardware
behavior, chosen behavior, reason, affected games, and verification. For a ROM patch also record the exact ROM hash,
file offset or bank/address, original bytes, replacement bytes, and the effect on later disassembly.
