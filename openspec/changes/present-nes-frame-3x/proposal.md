# Proposal

## Why

The PPU currently records register writes and returns alternating status bytes. Build NES graphics in stages so
the first image appears early and each new register effect or rendering behavior can be verified on its own.

## What Changes

Implement the graphics sequence below within this change. Each task introduces one hardware behavior or
one host prerequisite with its own verification. The [tasks](tasks.md) start with presentation of supplied
frames and proceed through PPU-generated frames, background, timing, and sprites.

## PPU Graphics Roadmap

Keep CPU access to the PPU registers routed through Machine. Machine connects the PPU to the cartridge's CHR ROM
and to 2 KiB of nametable VRAM (CIRAM). The PPU uses its own address space for CHR, nametables, and palette RAM.
Sprite attributes live in the PPU's separate OAM. pygame presents the finished frame at the host boundary.

1. **Show a test frame in pygame.** Accept a complete 256 × 240 RGB frame and present it in a 768 × 720 drawing
   area. Verify that every source pixel occupies an exact 3 × 3 block and that subsequent frames reuse the window.
2. **Connect video memory and show the first PPU color.** Connect the fixed 8 KiB NROM CHR ROM, map nametable
   VRAM with the cartridge's horizontal or vertical mirroring, and add palette RAM. Introduce the two-write
   address port (`$2006`) and data writes (`$2007`) in small steps. Verify the address latch reset on
   `$2002` reads and the data increment of 1 or 32 selected by `$2000`. A synthetic program writes `$3F00`
   and displays the resulting backdrop before background or sprite rendering is available. Introduce buffered
   `$2007` reads as a separate behavior after that visible milestone.
3. **Draw a stationary background.** Read tile numbers from the nametable and pixel indices from the pattern
   table selected by `$2000`. Use palette RAM for colors. Add attribute-based palette selection, then
   `$2005` scrolling and nametable crossings, with focused synthetic scenes for each behavior.
4. **Advance frames and let the game leave its startup wait.** Replace alternating `$2002` values with vblank
   based on nominal emulated CPU cycles. Verify that a status read clears the vblank flag. Introduce CPU NMI
   entry and connect the PPU's NMI request to the enable bit in `$2000` as separately verified steps. Open the
   pygame window at cartridge startup and present completed emulator frames there.
5. **Draw sprites and combine layers.** Add OAM access (`$2003/$2004`) and DMA (`$4014`) as separate behaviors.
   Draw 8 × 8 and 8 × 16 sprites from OAM and CHR, then verify transparency, flips, and priority. Exercise all four
   `$2001` layer combinations: backdrop only, background only, sprites only, and both layers. Add the left
   eight-pixel masks, grayscale, and color emphasis separately.

Use whole-frame rendering at first. If a game depends on mid-frame changes or the timing of a sprite-zero hit,
give that behavior its own verification step. After each game-facing change, rerun Battle City and use the next
observed obstacle to order the remaining work. The current startup wait depends on NMI. The Battle City NMI
handler writes `$4014` at `$D40D`, so OAM DMA may be needed before the first game frame.
[Local ROM checks](../../../ROMs/README.md) · [Battle City listing](../../../doc/disassembly/BattleCity.asm)

## Capabilities

### New Capabilities

- `nes-frame-display`: Present a native-size NES frame in a pygame window at fixed integer scale 3.
- `ppu-memory`: Expose NROM pattern data, mirrored nametable VRAM, and palette RAM to the PPU.
- `ppu-rendering`: Compose the backdrop, background, and sprites using PPU state and display controls.

### Modified Capabilities

- `ppu-registers`: Give mirrored video registers their selected memory, status, scroll, and NMI effects.
- `cpu-memory`: Route readable PPU data ports and OAM DMA through Machine.
- `cpu-execution`: Service a functional NMI entry through the CPU stack and vector.
- `emulator-control`: Advance PPU timing at instruction boundaries and publish completed frames.
- `emulator-cli`: Start the graphical run when a cartridge path is supplied.

## Impact

The work touches the PPU, its attached memory, Machine routing, CPU interrupt entry, and the host execution loop.
The first milestone uses the existing pygame dependency. Run a cartridge in the window with `python main.py ROM`.
The common tests use synthetic cartridges, and bounded local executions track the next game obstacle.
