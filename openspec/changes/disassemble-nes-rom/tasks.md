# Tasks

## 1. Decode PRG bytes

- [x] 1.1 Load mapper-0 PRG without constructing Machine; verify 16 KiB, 32 KiB, trainer, and unsupported layouts
  with synthetic cartridge tests.
- [x] 1.2 Decode all 151 official opcode/mode combinations using an independent reference; verify their mnemonics,
  lengths, operands, and bytes, plus `db` continuation and incomplete final instructions, with focused pytest cases.
- [ ] 1.3 Collect direct branch, `JMP`, and `JSR` targets in a first pass and emit labels in a second; verify forward,
  backward, repeated, indirect, out-of-range, and mid-instruction targets with synthetic programs.

## 2. Produce readable listings

- [ ] 2.1 Add exact-address `EQU` aliases for 16 KiB mirrors; verify both control-flow and data operands preserve the
  lower address while each PRG byte appears only once.
- [ ] 2.2 Symbolize the specified PPU, APU, DMA, and controller addresses; verify PPU mirrors, $4017, indexed operands,
  immediate values, and hardware-address control targets with focused tests.
- [ ] 2.3 Add the two-path standalone CLI and source-overwrite protection; verify paths with spaces, another working
  directory, unsupported layouts, output contents, and unchanged input using subprocess tests.
- [ ] 2.4 Document the command, output, address windows, unsupported bytes, and linear-decoding limitations in
  `README.md` and `doc\disassembly\README.md`; record the design rationale in `doc\decisions.md`.

## 3. Integration

- [ ] 3.1 Run the disassembler and cartridge-loading pytest cases together and verify the resulting listing accounts for
  every PRG byte without relying on local game ROMs.
