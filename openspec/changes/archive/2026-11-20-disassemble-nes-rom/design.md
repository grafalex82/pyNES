# Design

## Context

`NESFile` exposes PRG bytes separately from trainer and CHR bytes. `Machine` maps ordinary mapper-0 PRG as either
16 KiB mirrored twice or 32 KiB mapped once; its execution devices are unnecessary for offline disassembly.
The CPU handler table is incomplete and describes execution, not a complete static decoder.

## Goals / Non-Goals

**Goals:**

- Make a reproducible listing from the actual PRG bytes without starting a CPU.
- Keep every selected PRG byte visible, including bytes that cannot form an official instruction.
- Preserve exact CPU addresses even when a target is a mirror or does not coincide with a listing line.

**Non-Goals:**

- Distinguish all executable code from data, infer indirect targets, or guarantee a correct control-flow graph.
- Support unofficial opcodes, other mappers, game patches, execution, or round-trip assembly.
- Produce a manually annotated game listing or depend on a locally installed game ROM.

## Decisions

### Standalone cartridge inspection

Add `misc/disassemble.py`, using the same script-relative `src` import approach as `misc/nesinfo.py` and accepting
the input and output paths as positional arguments. Reuse `NESFile` for parsing, including its existing unsupported
format errors, and consume only the PRG section. Reject unsupported mapper/submapper or PRG size explicitly.
An extracted trainer does not affect the PRG byte layout here; unlike Machine, the tool does not map trainer memory.
Protect the input from being selected as the output before writing.

Constructing Machine or running CPU was considered, but neither is needed to decode immutable PRG bytes; that approach
would also couple the listing to unimplemented execution and device behavior.

### Fixed address windows

Use $8000 as the listing base for a 32 KiB section and $C000 for a 16 KiB section. Hardware exposes a 16 KiB NROM
image in both windows; the lower half is an alias, not additional file content. When an operand references its
$8000-$BFFF alias, emit an `EQU` symbol with that exact address and identify the mirrored upper address in a comment.
Do not silently rewrite the operand to the upper window. Other operands and immediate values keep their actual
encoded meaning. Outputting both windows was considered, but duplicates the entire listing.

### Independent two-pass decoding

Keep a compact opcode-to-mnemonic and addressing-mode table for all 151 official encodings in the utility.
Do not derive it from CPU handlers or execute instructions. On the first linear scan, decode instruction boundaries
from the selected base and collect relative branches, direct absolute `JMP` and `JSR` targets, and needed address
symbols. Calculate a relative target from the next instruction address plus its signed displacement, wrapped to 16 bits.
`JMP (address)` names a pointer, not its runtime destination, and does not create an inferred control-flow target.

Repeat the same decoding on the second scan to emit bytes, mnemonics, operands, and definitions for collected labels.
Unknown opcode bytes are displayed as `db` and advance one byte. If a valid opcode lacks its complete operand at the
end of PRG, emit each remaining byte as `db`. This is a listing convention for arbitrary data, not a claim that the
emulator implements an unknown instruction; CPU execution retains its existing `NotImplementedError` behavior.

Recursive traversal was considered, but it requires control-flow inference, still cannot resolve every indirect jump,
and does not meet the selected simple linear-listing approach.

### Symbols without changing addresses

Use deterministic labels based on the exact target address and define each label once. Put labels at decoded line
boundaries; use `EQU` for targets inside another instruction, outside the selected window, or in a mirrored window.
The same byte may be the target of several distinct CPU addresses; these remain distinct symbols.

For a complete mapper-0 PRG, read the final three little-endian words at $FFFA-$FFFF as the NMI, reset, and IRQ
vectors. Name their exact targets `NMI`, `START`, and `IRQ`, respectively, even when multiple vectors share a target.
Define each name at a decoded line boundary or with `EQU` otherwise; 16 KiB lower-mirror targets retain the encoded
address. Keep existing direct-branch labels when they share an address with a vector. Vector targets in hardware space
use the corresponding hardware symbol in their `EQU` definition. Continue the existing linear scan across the vector
bytes without inventing code boundaries or omitting any PRG bytes.

Use standard named CPU-visible PPU, APU, OAM DMA, and controller registers in operand expressions, with `EQU`
definitions for the referenced names. PPU registers repeat every eight addresses through $3FFF; preserve the encoded
mirror address in the expression or its definition. Keep read/write-sensitive shared addresses such as $4017
unambiguous, and do not treat immediate constants or computed indexed effective addresses as known registers.
When a control target is also a hardware address, define its target label through the hardware symbol so both the
exact target label and register name remain visible.

### References

Use the [MCS6500 programming manual](https://syncopate.us/books/Synertek6502ProgrammingManual.html) for the documented
instruction encodings and addressing modes. The existing [CPU memory specification](../../specs/cpu-memory/spec.md)
records the project's NROM mapping; [Mesen's NROM mapper][mesen-nrom] and [py65's vector locations][py65-vectors] were
consulted for comparison, not as code to copy.

[mesen-nrom]: https://github.com/SourMesen/Mesen2/blob/master/Core/NES/Mappers/Nintendo/NROM.h
[py65-vectors]: https://github.com/mnaberez/py65/blob/main/py65/devices/mpu6502.py

## Risks / Trade-offs

- [Data decoded as code] -> Keep original bytes and document that labels and boundaries are hypotheses.
- [Indirect or dynamically computed control flow] -> Do not invent targets; users must investigate them separately.
- [16 KiB mirror or non-boundary target] -> Define an exact-address `EQU` instead of forcing a misleading line label.
- [Unsupported byte in arbitrary data] -> Show one `db` byte and continue; retain all remaining PRG bytes.
- [Source and output refer to the same file] -> Refuse to write, preserving the original cartridge.

## Migration Plan

No migration or existing API change is required. The utility is invoked explicitly; removing it reverses the addition.
