# Spec Delta

## Purpose

Export the tiles stored in a cartridge's 8 KiB CHR ROM as two PNG sheets for offline inspection, without emulating
the cartridge or reconstructing a game screen.

## ADDED Requirements

### Requirement: Export two CHR ROM sheets

The `chr2png.py` command SHALL accept a supported `.nes` cartridge path and an output path prefix. For a cartridge
with exactly 8 KiB of CHR ROM it SHALL write `<prefix>-0000.png` for the first 4 KiB and `<prefix>-1000.png` for
the second 4 KiB. Relative paths SHALL resolve from the caller's working directory. Outputs SHALL be distinct from
each other and SHALL NOT overwrite input files.

#### Scenario: Export from another working directory

- **WHEN** the command is invoked from another working directory with a relative cartridge path containing spaces
  and the output prefix `chr`
- **THEN** it writes `chr-0000.png` and `chr-1000.png` in that directory for the two CHR halves in file order
- **AND** the input cartridge is unchanged

#### Scenario: Reject an output that aliases an input

- **WHEN** either destination identifies the input cartridge or selected palette file
- **THEN** the command reports a path conflict, exits unsuccessfully, and writes neither PNG

### Requirement: Reject unsupported CHR ROM sizes

For a supported cartridge with no CHR ROM or with a CHR ROM size other than 8 KiB, the command SHALL report the
unsupported size and exit unsuccessfully without creating or replacing either output.

#### Scenario: Cartridge lacks CHR ROM

- **WHEN** the cartridge declares zero bytes of CHR ROM
- **THEN** the command reports that there is no CHR ROM and writes neither PNG

#### Scenario: Cartridge has more than two sheets of CHR ROM

- **WHEN** the cartridge has 16 KiB of CHR ROM
- **THEN** the command reports that only 8 KiB is supported and writes neither PNG

### Requirement: Preserve tile pixels and storage order

Each sheet SHALL show all 256 tiles from its CHR half in a 16-column by 16-row grid, in file order from left to right
and top to bottom. Each tile SHALL be an 8-by-8 pixel pattern. The four pixel values SHALL follow the two CHR
bitplanes, with the first plane providing the low bit, the second plane providing the high bit, and bit 7 at the left.

#### Scenario: Decode asymmetric patterns on both sheets

- **WHEN** the CHR halves contain different known tile patterns with both bitplanes in use
- **THEN** the first and last tile positions on each sheet show the corresponding patterns in the correct orientation
- **AND** the colors correspond to the decoded values 0 through 3 in the selected palette

### Requirement: Select a preview palette

The command SHALL use the same four opaque grayscale levels on both sheets by default. `--palette` and
`--palette-file` SHALL be mutually exclusive and accept the same whitespace-separated list of exactly four or eight
two-digit hexadecimal NES color codes (`00` through `3F`, case-insensitive). Four codes SHALL apply to both sheets;
eight SHALL supply four codes per sheet in output order. Within each group, codes SHALL map pixel values 0 through 3
to opaque RGB colors.

#### Scenario: Use the default palette

- **WHEN** the command is invoked without a palette option
- **THEN** both sheets map the four pixel values to the same four distinct opaque levels, from black to white

#### Scenario: Apply one palette provided inline

- **WHEN** the command receives `--palette "0F 01 21 30"`
- **THEN** both sheets map pixel values 0 through 3 to those four colors in the specified order

#### Scenario: Use a palette file for two different palettes

- **WHEN** a UTF-8 palette file contains `0F 01 21 30` on one line and `0F 06 16 26` on the next
- **THEN** using `--palette-file` produces the same pixels as providing all eight codes through `--palette`
- **AND** the first group colors the `-0000.png` sheet and the second group colors the `-1000.png` sheet

#### Scenario: Reject invalid or conflicting palette arguments

- **WHEN** a palette has an invalid code or count, or the command receives both palette options
- **THEN** the command reports the argument error and writes neither PNG

### Requirement: Keep dotted separators one pixel wide

The PNGs SHALL have one-pixel gray dotted gutters between adjacent rows and columns, without an outer border or
changes to tile pixels. The gaps between gray dots SHALL be transparent. The default scale SHALL be 1. With
`--scale 2`, each tile pixel SHALL be duplicated to a 2-by-2 block of the same color without smoothing or enlarging
the gutters. The command SHALL reject scale values other than 1 and 2.

#### Scenario: Inspect a native-sized sheet

- **WHEN** the command is run at the default scale
- **THEN** each PNG is 143 by 143 pixels and its tiles are 8 by 8 pixels
- **AND** gray dots alternate with transparent pixels in the horizontal and vertical one-pixel gaps

#### Scenario: Inspect a doubled sheet

- **WHEN** the command is run with `--scale 2`
- **THEN** each PNG is 271 by 271 pixels and every tile is 16 by 16 pixels
- **AND** each source pixel is represented by four identical pixels, while the dotted gutters remain one pixel wide
