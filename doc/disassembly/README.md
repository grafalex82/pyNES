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

Each generated instruction line shows its CPU address, one to three original bytes, mnemonic, and operands. For
example, an unannotated excerpt could look like this:

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

Analyze only the part the user selects, one piece at a time. Questions about the code, architecture, or peripherals
may instead be explored in discussion; do not automatically annotate additional sections. Identify each source ROM
before assigning fixed addresses or interpreting routines.

For each listing, record the ROM filename, SHA-256, revision when known, mapper, and relevant bank layout. Distinguish
CPU addresses from file offsets and bank-relative locations. Include instruction bytes so observations can be checked
against the original file.

These files are annotated listings for people to read, not conventional assembly source or input to an assembler.
Use English for names and explanations.

- Leave unexamined instruction lines starting in column 1. Indent analyzed instruction lines by four spaces, so
  reviewed and unreviewed instructions are easy to distinguish. Indent comments describing code blocks by four spaces.
  Place labels, function comments, other full-line comments, variable declarations, and data directives at column 1.
- Start inline comments in column 40.
- Preserve each instruction's address, original bytes, mnemonic, and operand information, including its addressing
  mode. A meaningful name may replace a generated label or numeric operand without changing the encoded address.
- Give variables and labels meaningful names of at most 16 characters. When an instruction uses a named variable or
  jump target, include its address in parentheses alongside the name, including for hardware register names. An
  instruction comment can hold this address without confusing it with 6502 indirect addressing syntax.
- Describe each variable in a comment: its role, possible values, and the functions that use it. State what is unknown
  rather than presenting a hypothesis as fact.
- Separate logical blocks with at least one blank line and a short comment describing what each block does. Separate
  functions with a full-line comment describing the function, its parameters, and its results.
- Identify data that the linear disassembler mistook for code and represent it as `db` blocks, or `dw` for 16-bit
  values such as vectors. Manually decode instructions when necessary, retaining the original addresses and bytes.

For example, the following is a synthetic illustration of formatting, not a claim about a game's code:

```text
; GameState ($0010): Current state; values and users are not yet known.
GameState EQU $10

; MainEntry ($C000): Example routine; inputs and results are not yet known.
MainEntry:
    ; Call the initialization routine.
    $C000: 20 34 C0  JSR InitScreen    ; InitScreen ($C034)

    ; Read the current game state.
    $C003: A5 10     LDA GameState     ; GameState ($0010)

; Store example text as data.
ExampleText:
$C005: 41 42     db "AB"
```

Explain algorithms in adjacent Markdown when listing comments alone are insufficient. Do not overwrite an annotated
listing with regenerated output. Record patched bytes separately and cross-reference [the decisions](../decisions.md).
