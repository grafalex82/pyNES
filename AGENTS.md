# Working on pyNES

Read README.md, doc/development.md, doc/decisions.md, and openspec/config.yaml before proposing or implementing changes.
This is a learning project. Understanding each step matters more than reaching a playable game quickly.

## Scope and workflow

- DO NOT OVERENGINEER.
- Make one behavioral change at a time: one CPU instruction or one aspect of a peripheral.
- A prerequisite such as ROM header parsing is its own small change. Never bundle a complete emulator skeleton.
- Let the next observed `NotImplementedError` determine the next behavior once a game can be attempted.
- Stop after the selected behavior works and report the next obstacle. Do not automatically implement it.
- Keep unknown instructions, registers, and mapper behavior explicit with `NotImplementedError` and useful context.
- For cartridge file loading and inspection, assume valid input; omit corruption checks, repair, and exception handling.
- Deliberate simplifications, including audio responses, need an explanation and focused verification.
- Use OpenSpec for small changes. Read the relevant installed skill before using its workflow.
- Keep exploration, proposed behavior, and implemented capabilities distinct. Do not claim unimplemented features.
- Do not create an implementation change while the current request is only project setup or exploration.

## Architecture

- Keep the CPU, RAM, ROM, controllers, and other devices separate, with one Python module per component.
- Machine owns address routing and connects components. CPU memory and I/O requests always go through Machine.
- Use the same routing for memory-mapped I/O.
- Support single-instruction execution and bounded blocks as separate, incremental capabilities.
- Add internal address breakpoints with callbacks when that capability is introduced.
- Use standard logging with component loggers for instruction traces, post-instruction registers, and device events.
- Keep exact timing, physical video signals, and audio output outside the project scope.

## Code style

- Use English for identifiers, comments, docstrings, documentation, and disassembly explanations.
- Prefer simple classes and functions. Introduce shared interfaces or abstractions only for a demonstrated need.
- Keep code compact and avoid redundant defensive checks, compatibility layers, and unrelated cleanup.
- Limit lines to 120 characters. Do not wrap expressions or signatures that already fit.
- Leave two blank lines between functions, including methods.
- Leave one blank line between logical blocks inside a function.
- If a function has multiple logical blocks, add a one-line comment explaining each block.
- Explain hardware behavior, algorithms, and non-obvious choices; do not merely restate the Python code.
- Use Python, pygame, and pytest. Do not introduce pyenv or wheel-based packaging/build tooling.

## Verification and documentation

- Add focused pytest tests for the selected behavior, including relevant registers, flags, and memory effects.
- Use small synthetic programs and fixtures for unit tests; keep routine tests independent of local game ROMs.
- Run the relevant tests and report what was checked. Do not add tests just to exercise documentation or placeholders.
- Record decisions with their rationale in doc/decisions.md; retain proposals as proposals until selected.
- Document every departure from hardware behavior and every game patch, including its reason and affected ROM.
- Keep annotated disassembly under doc/disassembly/ and follow its README.md conventions for user-selected analysis.
- Identify ROM revisions and mapper requirements from actual files, not titles alone.
- Consult public references and other emulators for understanding, then explain and implement the behavior yourself.
- Do not copy another emulator's implementation as is.
- Do not download ROMs, fabricate execution results, or claim a game runs without checking it.

## Repository

Use doc/, src/, test/, resources/, ROMs/, and misc/ for the purposes described in README.md.
Keep local ROM images, generated traces, caches, and virtual environments out of version control.
Use the MIT license for original project code and documentation.
