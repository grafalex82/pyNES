# nes-rom-loading Specification

## Purpose

Read NES cartridge metadata and byte sections for future emulation and provide a small command-line inspection tool.

Inputs are assumed to be structurally valid cartridge files. Corrupt or truncated files have no guaranteed behavior;
ordinary Python exceptions and tracebacks are acceptable. Detecting or repairing corruption is outside this capability.

## Requirements

### Requirement: Inspect a selected ROM file

The inspection utility SHALL accept a positional ROM path and print its format, mapper/submapper, PRG/CHR and trainer
byte sizes, mirroring flags, and nonvolatile-memory flag. It SHALL exit normally after inspection without emulation.

#### Scenario: Inspect a path containing spaces

- **WHEN** the utility receives a supported valid ROM path containing spaces as one argument
- **THEN** it prints the decoded basic parameters and exits with status 0 without changing the file

### Requirement: Decode ordinary cartridge headers

The loader SHALL distinguish iNES from NES 2.0, decode ordinary PRG/CHR size counts including NES 2.0 extensions,
and expose the original header and complete mapper/submapper fields. The iNES submapper SHALL be 0.

#### Scenario: Load iNES metadata

- **WHEN** a valid iNES file declares PRG/CHR counts and mapper bits
- **THEN** sizes use 16384-byte PRG units and 8192-byte CHR units and all mapper bits are preserved
- **AND** the original header is available unchanged with submapper 0

#### Scenario: Load NES 2.0 metadata

- **WHEN** a valid NES 2.0 file uses ordinary size extensions and extended mapper/submapper fields
- **THEN** the result preserves those extensions and fields without requiring mapper emulation

### Requirement: Extract the cartridge byte sections

The loader SHALL expose the optional trainer, PRG ROM, and CHR ROM separately and preserve their source bytes.
Absent trainer and zero-length CHR sections SHALL be empty bytes; no emulated memory SHALL be allocated.

#### Scenario: Extract trainer and ROM data

- **WHEN** a valid image declares a trainer and distinct PRG/CHR sections
- **THEN** the result contains exactly the 512 trainer bytes and the declared PRG/CHR bytes in their proper sections

#### Scenario: Extract an image without a trainer or CHR ROM

- **WHEN** a supported image declares no trainer and zero CHR ROM bytes
- **THEN** those sections are empty and the declared PRG bytes are preserved

### Requirement: Expose basic cartridge flags

The loader SHALL expose the header's horizontal, vertical, or four-screen mirroring indication and its nonvolatile
memory flag for inspection. These values SHALL describe header metadata without claiming effective mapper behavior.

#### Scenario: Inspect header flags

- **WHEN** a valid file sets mirroring or nonvolatile-memory flags
- **THEN** the decoded values reflect those flags and can be displayed without constructing emulated devices

### Requirement: Keep unimplemented format features explicit

The loader SHALL raise NotImplementedError for unrecognized format markers, NES 2.0 exponent-multiplier sizes,
nonstandard console types, and declared miscellaneous ROM areas rather than interpreting them as implemented features.

#### Scenario: Encounter an unsupported feature

- **WHEN** a file declares any of these unimplemented format features
- **THEN** loading raises NotImplementedError identifying that feature
