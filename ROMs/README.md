# Local game ROMs

Place local game ROM images here when game exploration begins.
ROM images are ignored by Git. No images have been added or inspected during project setup.

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
