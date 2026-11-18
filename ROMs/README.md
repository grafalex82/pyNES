# Local game ROMs

Place local game ROM images here when game exploration begins.
ROM images are ignored by Git. No images have been added or inspected during project setup.

Before choosing mappers or producing listings, record each filename, SHA-256, ROM format, revision when known,
mapper ID, PRG/CHR sizes, and mirroring metadata. Use actual file contents rather than assumptions based on the title.

On Windows, a local image can be identified with:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'ROMs\your-game.nes'
```

Header inspection will be introduced as a separate small change if selected as the first implementation step.
