# Annotated game disassembly

## Generate a study listing

From the repository root, run the standalone utility with an iNES or NES 2.0 cartridge and an output path:

```text
python misc\disassemble.py "ROMs\your game.nes" "listing.asm"
python misc\disassemble.py --help
```

Quote paths containing spaces. Both paths are relative to the working directory; from another directory use the full
path to the script. The output is UTF-8 text with LF line endings. An existing output is overwritten, but paths
identifying the input cartridge, including aliases and hard links, are rejected before writing.

The utility accepts mapper 0, submapper 0, and 16 KiB or 32 KiB PRG. Unsupported layouts raise `NotImplementedError`.
It reads PRG without executing it; a trainer is accepted but not mapped or included, and CHR data is not listed.
A 16 KiB PRG appears once at $C000-$FFFF; references to its $8000-$BFFF mirror use exact-address `EQU` aliases.
A 32 KiB PRG appears once at $8000-$FFFF.

Each instruction line shows its CPU address, one to three original bytes, mnemonic, and operands. For example, an
excerpt could look like this:

```text
PPUCTRL EQU $2000

START:
$C000: A9 80     LDA #$80
$C002: 8D 00 20  STA PPUCTRL
L_C005:
$C005: 4C 05 C0  JMP L_C005
$C008: 02        db $02
```

The first linear pass collects relative branch and direct `JMP`/`JSR` targets; the second emits the same decoded
lines with `L_XXXX` labels and referenced PPU, APU, DMA, and controller symbols. Unknown opcode bytes and incomplete
final instructions are shown as individual `db` bytes. Every PRG byte, including the final six vector bytes, remains
in the listing exactly once.

The little-endian vector words at $FFFA, $FFFC, and $FFFE name their respective targets `NMI`, `START`, and `IRQ`.
Several names can mark the same address. Targets without a decoded line, including 16 KiB lower-mirror targets, use
`EQU` to preserve the encoded address; a hardware target uses the corresponding hardware symbol.

This is a study listing, not reassemblable source or a verified game disassembly. Linear scanning can interpret data
as instructions and miss genuine code boundaries. An indirect jump provides a pointer, not its runtime destination;
indirect and other computed targets are not inferred. Labels, including vector targets, do not prove that the bytes
at those addresses are executable code.

## Annotating game code

Game disassembly is deferred at the user's request. When it resumes, identify each source ROM before assigning fixed
addresses or interpreting routines.

For each listing, record the ROM filename, SHA-256, revision when known, mapper, and relevant bank layout. Distinguish
CPU addresses from file offsets and bank-relative locations. Include instruction bytes so observations can be checked
against the original file.

Use labels and English comments to explain what a routine computes, its inputs and outputs, important RAM variables,
device accesses, and its role in the game. Mark uncertain interpretations as hypotheses. Separate executable code
from data rather than assuming a linear sweep has identified every instruction correctly.

Expand listings as game execution reveals new routines. Explain algorithms in adjacent Markdown when assembly
comments alone are insufficient. Record patched bytes separately and cross-reference doc/decisions.md.
