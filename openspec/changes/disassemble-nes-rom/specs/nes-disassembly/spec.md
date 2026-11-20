# Spec Delta

## Purpose

Provide a readable offline listing of mapper-0 NES program bytes for studying 6502 code and hardware accesses.

## ADDED Requirements

### Requirement: Generate a listing from a cartridge

The standalone utility SHALL take a NES file path and an output file path as two positional arguments. It SHALL write
the listing to the output path without executing the program or modifying the source cartridge.

#### Scenario: Write a listing from another working directory

- **WHEN** the utility is called with supported input and output paths containing spaces from another directory
- **THEN** it writes the listing to the requested file and the source cartridge bytes remain unchanged

#### Scenario: Prevent overwriting the cartridge

- **WHEN** the output path identifies the input cartridge
- **THEN** the utility fails before writing and leaves the cartridge unchanged

### Requirement: Limit cartridge layouts explicitly

The utility SHALL accept supported iNES and NES 2.0 files with mapper 0, submapper 0, and a 16 KiB or 32 KiB PRG
section. It SHALL raise `NotImplementedError` identifying any unsupported mapper, submapper, or PRG size.

#### Scenario: Read a cartridge with a trainer

- **WHEN** a supported mapper-0 file contains a trainer, PRG ROM, and CHR ROM
- **THEN** the listing describes only PRG bytes, beginning after the trainer

#### Scenario: Reject unsupported cartridge wiring

- **WHEN** a cartridge declares another mapper or submapper, or a PRG size other than 16 KiB or 32 KiB
- **THEN** the utility raises `NotImplementedError` identifying the unsupported configuration

### Requirement: Show the CPU address of each PRG byte

The listing SHALL represent a 32 KiB PRG section once at $8000-$FFFF and a 16 KiB section once at $C000-$FFFF.
The lower $8000-$BFFF mirror of 16 KiB PRG SHALL use `EQU` aliases when referenced, preserving the actual address.

#### Scenario: Disassemble a 16 KiB mirrored cartridge

- **WHEN** an instruction targets $8000 in a 16 KiB PRG image
- **THEN** the listing shows that PRG byte at $C000 only and defines the $8000 target with an `EQU` alias

#### Scenario: Refer to mirrored PRG as data

- **WHEN** an instruction reads a 16 KiB cartridge through an absolute $8000-$BFFF address
- **THEN** its operand uses an `EQU` alias retaining that lower address

#### Scenario: Disassemble a 32 KiB cartridge

- **WHEN** a cartridge has a 32 KiB PRG section
- **THEN** the listing shows its first byte at $8000 and its last byte at $FFFF

### Requirement: Decode the official 6502 instruction set

The utility SHALL linearly decode all official MOS 6502 opcode and addressing-mode combinations independently of
emulator instruction support. Each instruction line SHALL show its CPU address, one to three original bytes, mnemonic,
and any operands. The listing SHALL retain every PRG byte exactly once in its selected address range.

#### Scenario: Display instructions of different lengths

- **WHEN** PRG contains an implied, immediate, and absolute instruction in sequence
- **THEN** their lines show the respective one, two, and three bytes, correct addresses, mnemonics, and operands

#### Scenario: Display addressing modes

- **WHEN** official instructions use indexed, indirect, accumulator, or relative addressing
- **THEN** the operands distinguish those addressing modes and preserve their encoded values

### Requirement: Represent undecoded bytes as data

The utility SHALL represent each unofficial opcode byte as `db` with its address and value and continue scanning.
An official opcode lacking all operand bytes at the end of PRG SHALL also be represented as individual `db` bytes.

#### Scenario: Continue after an unofficial opcode

- **WHEN** an unofficial opcode byte precedes an official instruction
- **THEN** the listing shows the byte as `db` and decodes the following instruction at the next address

#### Scenario: Handle an incomplete final instruction

- **WHEN** the final PRG bytes begin an official instruction but do not contain its complete operands
- **THEN** each remaining byte appears as `db` rather than reading beyond PRG or discarding a byte

### Requirement: Label directly encoded control-flow targets

The utility SHALL collect direct relative branch and absolute `JMP` and `JSR` targets in a first linear pass.
The second pass SHALL use one stable label per distinct target in the instruction operands and define each label
at the corresponding line, or with `EQU` if there is no corresponding line in the selected address range.

#### Scenario: Reuse a forward target label

- **WHEN** two direct branches target the same later instruction
- **THEN** both operands use the same label and that instruction has one matching label definition

#### Scenario: Calculate a backward relative target

- **WHEN** a relative branch has a negative signed displacement
- **THEN** its label identifies the 16-bit address calculated from the address following the branch

#### Scenario: Target does not coincide with a listing line

- **WHEN** a direct target falls inside another decoded instruction or outside the listed PRG range
- **THEN** an `EQU` label preserves the exact target address instead of inventing an instruction boundary

#### Scenario: Indirect jump destination is not encoded

- **WHEN** the listing contains an indirect `JMP`
- **THEN** it shows the encoded pointer operand without inventing a direct target label for its runtime destination

### Requirement: Name the CPU vector targets

The listing SHALL read the little-endian NMI, reset, and IRQ vector words at $FFFA, $FFFC, and $FFFE from a complete
mapper-0 PRG section and define their exact targets as `NMI`, `START`, and `IRQ`, respectively. Vector bytes SHALL
remain in the linear listing exactly once. Existing labels for directly encoded control-flow targets SHALL remain
available when they share an address with a vector.

#### Scenario: Name all vector targets

- **WHEN** a supported PRG contains three different vector addresses at decoded line boundaries
- **THEN** those lines have the corresponding `NMI`, `START`, and `IRQ` labels

#### Scenario: Multiple vectors share a target

- **WHEN** two or more vectors encode the same address
- **THEN** every applicable vector name is defined at that address

#### Scenario: A vector target has no listing line

- **WHEN** a vector targets the middle of a decoded instruction, an address outside the listed window, or a 16 KiB
  lower PRG mirror
- **THEN** its named `EQU` definition preserves the exact encoded address rather than inventing a line boundary

#### Scenario: A vector targets a hardware register

- **WHEN** a vector encodes a known hardware address
- **THEN** its name is defined through the hardware symbol for that exact address

### Requirement: Name known memory-mapped hardware registers

The listing SHALL define symbolic names using `EQU` for referenced NES PPU, APU, DMA, and controller register
addresses and use the names in address operands. PPU mirror references SHALL retain their original CPU addresses.
The known addresses SHALL include PPU $2000-$2007 and its mirrors, APU $4000-$4008, $400A-$400C, $400E-$4013,
$4015, and $4017, DMA $4014, and controller ports $4016-$4017. Immediate values SHALL NOT be treated as addresses.

#### Scenario: Symbolize a PPU register reference

- **WHEN** an instruction directly addresses $2000
- **THEN** its operand uses a symbol defined with `EQU` as $2000 rather than the numeric address

#### Scenario: Preserve a PPU mirror address

- **WHEN** an instruction addresses $2008, a mirror of $2000
- **THEN** its symbolic operand and definitions retain the exact encoded address $2008

#### Scenario: Do not symbolize an immediate value

- **WHEN** an immediate operand equals the low byte of a known hardware address
- **THEN** it remains an immediate numeric value rather than a register symbol

### Requirement: Identify the limits of linear decoding

The utility documentation SHALL explain that a linear pass can mistake data for instructions, miss genuine code
boundaries, and cannot determine every indirect or runtime-computed target. The output SHALL be described as a
study listing, not a verified disassembly or reassemblable source file.

#### Scenario: Interpret generated output

- **WHEN** a user reads the utility documentation
- **THEN** the limitations and the distinction from a manually verified annotated disassembly are clear
