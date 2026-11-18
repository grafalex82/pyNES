# Local game ROMs

Keep local game ROM images here; they are ignored by Git.

Before choosing mappers or producing listings, record each filename, SHA-256, ROM format, revision when known,
mapper ID, PRG/CHR sizes, and mirroring metadata. Use actual file contents rather than assumptions based on the title.

From the repository root, inspect a valid local image and calculate its SHA-256 on Windows:

```powershell
python misc/nesinfo.py "ROMs/your game.nes"
Get-FileHash -Algorithm SHA256 -LiteralPath 'ROMs\your game.nes'
```

Replace the example filename with your file and retain the quotes for paths containing spaces. The inspection utility
prints header metadata and section byte sizes without changing the image. It does not identify the game revision or
calculate hashes. A mapper number describes the file; it does not mean that mapper is emulated.

Use structurally valid iNES or supported NES 2.0 files. Unsupported declared features raise `NotImplementedError`;
corrupt-input detection and repair are outside scope, and filesystem/parsing exceptions propagate normally.

## Inspected local files (2026-11-18)

All three headers declare mapper 0, submapper 0, no trainer, and no nonvolatile memory. Their mapper/submapper, trainer,
and PRG-size declarations fall within [Machine's current construction limits](../doc/memory.md#supported-configuration).
Byte routing is verified with synthetic cartridges. CPU reset and execution remain future work; no local game execution
is claimed. Filenames are local labels; exact game revisions have not been confirmed.
Each CLI inspection matched the expected metadata and left the full-file SHA-256 unchanged.

### BattleCity (Japan).nes

- Format: NES 2.0; PRG: 16384 bytes; CHR: 8192 bytes; mirroring: horizontal.
- Header: `4e 45 53 1a 01 01 00 08 00 00 00 00 00 00 00 01`.
- SHA-256: `166ec235b062aa337045832843e2916f96f12dcf08972ad747016dbe77db761c`.

### Space Invaders (J) [!].nes

- Format: iNES; PRG: 16384 bytes; CHR: 8192 bytes; mirroring: horizontal.
- Header: `4e 45 53 1a 01 01 00 00 00 00 00 00 00 00 00 00`.
- SHA-256: `64cda6bfa0cd154dfbe8ad169a98eb3fa818548c19b8840fab5621645bf5a31f`.

### Super Mario Bros. (Europe).nes

- Format: NES 2.0; PRG: 32768 bytes; CHR: 8192 bytes; mirroring: vertical.
- Header: `4e 45 53 1a 02 01 01 08 00 00 00 00 01 00 00 01`.
- SHA-256: `ff69421b584ce898b3d4b3ab57202900c079c45cdface84d654d0368ad796ffe`.
