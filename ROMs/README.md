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
Byte routing is verified with synthetic cartridges. These inspection checks did not execute games.
Filenames are local labels; exact game revisions have not been confirmed.
Each CLI inspection matched the expected metadata and left the full-file SHA-256 unchanged.

Earlier bounded entry checks on 2026-11-19 confirmed the recorded hashes for all three images before and after
execution. Each stopped at an unconnected PPU register.

After implementing minimal PPU register access, each image was run again with a 10,000-cycle budget. All stopped on
an unsupported CPU opcode before reaching the budget:

| Local image | Reset PC | Completed cycles | First unimplemented opcode | Address |
| --- | --- | ---: | --- | --- |
| BattleCity (Japan).nes | $C070 | 63 | $20 | $C089 |
| Space Invaders (J) [!].nes | $8000 | 54 | $86 | $801E |
| Super Mario Bros. (Europe).nes | $8000 | 44 | $BD | $8018 |

All three files matched their recorded SHA-256 hashes before and after these checks. No image was modified, and the
entry checks do not establish game playability.

On 2026-11-20, bounded checks with a budget of 1,000,000 CPU cycles stopped at these unimplemented memory writes:

| Local image | Completed cycles | First unimplemented write |
| --- | ---: | --- |
| BattleCity (Japan).nes | 158,498 | $4015 |
| Super Mario Bros. (Europe).nes | 37,018 | $4011 |

Both files matched their recorded SHA-256 hashes before and after execution. These checks do not establish playability.

After adding the dummy APU registers, bounded checks with the same 1,000,000-cycle budget stopped here:

| Local image | Completed cycles | First unimplemented behavior | Instruction address |
| --- | ---: | --- | --- |
| BattleCity (Japan).nes | 158,504 | Write to $4017 | $EA58 |
| Super Mario Bros. (Europe).nes | 56,705 | Opcode $EE | $804C |

Both files matched their recorded SHA-256 hashes before and after execution. No ROM was modified; neither result
establishes playability. The next missing behaviors are outside the dummy APU change.

After adding the dummy frame-counter write, BattleCity passed the $4017 write at $EA58. A 10,000,000-cycle bounded
run reached its budget without a `NotImplementedError`; its next instruction was $D8FA. The instructions at $D8F8
and $D8FA were each visited about 1.64 million times. They compare and wait for RAM $000B to change; the listing
identifies an increment in the NMI handler at $D43C. The current PPU does not generate NMI, so this wait cannot
progress through that mechanism. The next unsupported operation remains unknown. The ROM hash was unchanged, and
the bounded run does not establish playability.

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
