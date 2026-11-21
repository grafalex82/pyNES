# Design

## Context

The cartridge entry point runs bounded CPU blocks. The PPU can produce a backdrop frame from the palette, and
`FrameDisplay` can present it. See [the proposal](proposal.md) for the order of the graphics milestones.

## Goals / Non-Goals

Keep the PPU responsible for producing native-size pixels and the host responsible for presenting them. Each stage
adds one observable behavior at a time, with synthetic programs available before a game can produce a frame.
This model covers fixed NROM video wiring and whole-frame rendering at instruction-level timing.

## Decisions

1. **Accept packed RGB bytes.** Add `FrameDisplay` in `src/frame_display.py`, with `present(frame)` taking
   184,320 bytes. The format gives a synthetic fixture and a later frame producer the same contract. Passing a
   pygame Surface would also carry the pixels, with the producer then responsible for constructing that object.
2. **Scale at presentation.** Create one ordinary pygame window using `pygame.display.set_mode((768, 720))`.
   Turn the supplied bytes into a native-size RGB surface with `pygame.image.frombytes`. Use
   `pygame.transform.scale` to produce the 3× surface, blit it to the display surface, and flip the display.
   This replicates pixel colors without interpolation. Direct 3 × 3 rectangle drawing would require a Python call
   per source pixel.
   [pygame transform documentation](https://www.pygame.org/docs/ref/transform.html#pygame.transform.scale)
3. **Keep the window open across presentations.** Initialize the pygame display subsystem when creating the
   presenter and reuse the display surface across frames. The caller owns the event loop and display shutdown.
   A Python usage example can pump events and close the display after showing a synthetic frame.
   Show actual presentations per elapsed wall-clock second in the title, updating about once per second even when
   no frame was presented. Count the initial preview and do not pace emulation or count skipped PPU frames.
4. **Attach memory to the PPU.** Machine supplies an 8 KiB CHR ROM and 2 KiB nametable RAM using the existing
   ROM and RAM components. The PPU selects CHR, mirrored nametable RAM, or internal palette RAM from a 14-bit
   address. Keep OAM separate from that address space. Resolve unsupported video configurations only on the
   affected video path so PRG-only synthetic callers can still construct a Machine.
5. **Implement the CPU-facing ports.** Keep PPU register mirrors in Machine. In the PPU, track the current
   and temporary video addresses, fine horizontal scroll, and the shared first/second write toggle. A second
   address write copies the temporary address into the current address. Introduce the status read's toggle
   reset with that port, then switch bit 7 to emulated vblank when frame timing is available. Use one PPUDATA
   read buffer. DMA copies an addressed CPU page through Machine into OAM with the existing OAM write behavior.
   [PPU register behavior in Mesen 2](https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesPpu.cpp)
6. **Open the cartridge window early.** Load the cartridge and open the window before the first CPU block.
   Present the first backdrop frame, then sample `PPU.render_frame()` between bounded execution blocks.
   This makes current palette and VRAM changes visible before video timing is available. The host processes
   pygame events between blocks and releases the display on close or on a propagated execution error. Handle
   command-line help before display initialization.
7. **Advance video at instruction boundaries.** Use a fixed NTSC-derived period of 29,781 nominal CPU cycles,
   starting vblank at cycle 27,394 and clearing it at 29,667. Advance the phase by the elapsed cycles of
   each completed instruction. Set PPUSTATUS bit 7 at vblank entry regardless of NMI enable. A status read
   clears the flag while preserving the phase.
8. **Present completed frames in the existing window.** When frame output is enabled, capture one frame at
   each vblank entry. The host presents new completed frames in place of sampling between blocks. A synthetic
   ROM can verify this transition by changing the backdrop with NMI disabled.
9. **Build the image in layers.** A backdrop frame is sufficient to verify the first palette write from a
   synthetic CPU program. Decode background tiles from CHR and obtain palette selection from the attribute
   quadrants. Retain each background pixel's opacity when composing sprites so the sprite's priority applies
   even if its RGB color equals the backdrop. Select the first nontransparent sprite candidate in OAM order
   before resolving its background priority. Use a fixed RGB palette for output and apply the mask bits during
   composition. For the first NTSC profile, approximate each emphasis bit by reducing the other two RGB
   channels to three quarters of their previous value, using integer arithmetic.
10. **Deliver NMI after frame capture.** Service a pending NMI at the completed instruction's boundary and
    charge its seven nominal cycles to CPU and PPU progress without fetching a handler opcode as part of entry.
    Capturing at vblank entry places an NMI handler's video writes in the following frame.

## Risks / Trade-offs

- The SDL dummy driver can verify dimensions, colors, and surface reuse in pytest. A desktop smoke check can
  verify the actual window and confirm that it can be closed from the event loop.
- The early window samples the current PPU state at host execution boundaries. Palette or VRAM updates can
  become visible at those boundaries until frame delivery switches to emulated vblank.
- Whole-frame sampling uses one state for the image. Mid-frame scroll or palette changes, sprite-zero hits,
  and per-scanline sprite evaluation can affect games that depend on raster timing. The first pass composes
  eligible sprites in OAM order and leaves those timing-dependent behaviors for a separately observed need.
- The functional model reports zero for the unmodeled status and open-bus bits, stores OAM bytes directly,
  and performs DMA without a CPU stall. PPUDATA increments stay functional during rendering, and palette reads
  return raw six-bit codes. The backdrop always comes from `$3F00`, including when rendering is disabled.
  ROM write errors make invalid CHR writes visible as emulator diagnostics. Record each effect as it is added.
- The first cycle profile approximates NTSC timing. Test the local mapper-0 Battle City image first and record
  observed stops. PAL timing and sub-instruction NMI races require separate verification if a game needs them.
