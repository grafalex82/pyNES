# Design

## Context

See [proposal.md](proposal.md) and [the capability spec](specs/nes-rom-loading/spec.md).
The repository has no implementation yet. A local NES 2.0 file was inspected: mapper/submapper 0, PRG 16384 bytes,
CHR 8192 bytes, and no trainer. The user requested a standalone inspection utility and accepts crashes on invalid input.

## Goals / Non-Goals

**Goals:**

- Separate cartridge file data from future emulated memory devices.
- Support ordinary iNES and NES 2.0 sizes with compact, readable code.
- Print enough metadata to understand how the cartridge will later connect to Machine.

**Non-Goals:**

- Corruption detection, file repair, compatibility heuristics, and exception presentation.
- CPU startup, memory mapping, mapper emulation, and graphics initialization.

## Decisions

### A parsed file object and a separate utility

Use a plain `NESFile` class in `src/nesfile.py`, constructed from a filename. Read once and expose `header`, `format`,
`mapper`, `submapper`, `trainer`, `prg_rom`, `chr_rom`, `mirroring`, and `battery`. Sections use immutable bytes.
Derive reported sizes from section lengths. Keeping the header permits later interpretation of optional metadata.
This class holds cartridge data; later changes can wrap the data in ROM devices without involving this utility.
A single small class is sufficient; no parser framework, inheritance, or custom exceptions are needed.

Put the CLI in `misc/nesinfo.py`, reserving emulator startup for later. Use standard argument parsing and locate `src`
relative to the utility's own file so the utility also works when called from another directory. Print the format,
mapper/submapper, PRG/CHR and trainer byte counts, mirroring, and the nonvolatile-memory flag, then return normally.

```text
python misc/nesinfo.py "path/to/cartridge.nes"
```

### Decode only the selected format features

Use the format marker in header byte 7 to distinguish iNES and NES 2.0. Ordinary PRG/CHR counts use 16384/8192-byte
units; NES 2.0 adds size extension fields. Preserve complete mapper/submapper values without selecting mapper devices.
Interpret mirroring with the conventional header labels; a future mapper may control the effective layout instead.
Read trainer, PRG, and CHR at their declared file offsets. Keep absent sections empty; do not allocate CHR RAM.

Raise NotImplementedError for unsupported format markers, exponent-multiplier sizes, nonstandard consoles, and declared
miscellaneous ROM areas. These guards identify missing behavior, not corrupt input. Preserve other header fields
without interpreting them, including a valid nonzero expansion-device field.

References: [iNES](https://www.nesdev.org/wiki/INES) and [NES 2.0](https://www.nesdev.org/wiki/NES_2.0).

### Trust the input and let failures propagate

The user explicitly accepts failures on damaged files. Do not check signatures, lengths, section completeness,
trailing bytes, or file extensions, and do not repair headers. Read and slice directly using declared sizes.
Do not catch filesystem or parsing errors in the utility, suppress tracebacks, or standardize error exit codes.
This keeps the educational code focused on file structure; damaged-input behavior is deliberately unspecified.

### Test useful file behavior

Use synthetic headers and distinct trainer/PRG/CHR bytes in pytest temporary directories. Verify both formats,
ordinary size extensions, mapper/submapper bits, trainer offsets, empty sections, mirroring, nonvolatile memory,
and explicit NotImplementedError cases. Do not add a damaged-file test matrix or test argument-parser internals.
Run CLI subprocess tests from another directory with paths containing spaces. Automated tests do not require games.
Add minimal `pytest.ini` and `requirements.txt` files; runtime loading needs only the standard library.

## Risks / Trade-offs

- Damaged files may crash or expose incomplete sections -> Accepted for this project; behavior is unspecified.
- Header flags can differ from effective mapper behavior -> Present them as metadata only.
- Wrong offsets can look plausible -> Compare exact source bytes in focused tests.
- Supported parsing does not imply a playable cartridge -> Keep the utility separate from emulator startup.

## Migration Plan

This is the first loader implementation. Add the utility, loader, tests, and documentation without changing ROM files.
