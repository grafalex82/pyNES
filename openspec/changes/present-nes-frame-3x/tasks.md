# Tasks

## 1. Present supplied frames

- [x] 1.1 Implement `FrameDisplay` and verify with synthetic pytest frames that the 768 × 720 drawing area
      contains exact 3 × 3 copies of differing pixels in adjacent rows and columns and at the bottom-right corner.
- [x] 1.2 Verify in pytest that presenting a second frame reuses the display and replaces its old pixels.
- [x] 1.3 Document a runnable synthetic-frame example in README.md and record the host-side scaling and window
      lifecycle decisions in doc/decisions.md. Run the example and confirm that it displays the frame and closes
      through the pygame event loop.

## 2. Connect PPU memory and display the first PPU-generated color

- [x] 2.1 Connect mapper-0 CHR ROM to the PPU. Verify reads at both pattern-table boundaries, immutable bytes,
      and an explicit error for unsupported CHR access. Check that PRG-only fixtures still execute.
- [x] 2.2 Connect the two physical nametable VRAM pages. Verify both cartridge mirroring arrangements,
      the $3000-$3EFF mirror, and separation from CPU RAM.
- [x] 2.3 Map six-bit palette RAM. Verify repeated mirrors and the four sprite palette aliases.
- [x] 2.4 Give $2006 its two-write address effect and reset the write toggle on $2002 reads. Test interrupted
      pairs and register aliases. Update doc/memory.md as the register effects replace the retained-write stub.
- [x] 2.5 Implement writes to $2007. Verify successive stores with both increments selected by $2000 bit 2.
- [x] 2.6 Render the backdrop from $3F00. Run a synthetic CPU program that writes the palette through Machine
      and show the resulting color using the stage 1 presenter. Assert its native and scaled RGB output in pytest.
- [x] 2.7 Add buffered reads from $2007. Verify CHR and nametable priming, immediate palette reads, the palette
      read's buffer refill, and increment behavior through register mirrors.

## 3. Open the emulator window and synchronize frames with vblank

- [x] 3.1 Open the 768 × 720 window before the first CPU block when running `python main.py ROM`.
      Show the initial PPU frame and refresh it from `PPU.render_frame()` between bounded execution blocks.
      Verify that a synthetic cartridge's palette writes update the visible color in the same window.
      Verify startup order, close events, failure cleanup with traceback propagation, and `--help` without display
      initialization. Document the command and the temporary frame sampling in README.md and doc/decisions.md.
- [x] 3.2 Advance the PPU by completed CPU cycles and derive $2002 bit 7 from the frame phase. Remove the temporary
      `_next_status` alternation and update its tests. Test status clearing, recurring vblank without polling, and
      zero-cycle runs. Document the timing and status approximation.
- [x] 3.3 Publish completed frames at each vblank entry and present them in the existing window.
      Replace between-block sampling. With NMI disabled, verify that a palette write between two vblanks
      changes the next presented frame. Update the frame scheduling notes in doc/decisions.md.
- [x] 3.4 Show actual presentation FPS in the window title. Verify elapsed-time calculation, intervals longer than
      one second, and host-loop integration; document the measurement without adding frame pacing.
- [x] 3.5 Disable logging by default and enable DEBUG output with `--debug`. Verify both modes and document the option.

## 4. Enable the game's NMI handler and display the background

- [x] 4.1 Add CPU NMI entry at an instruction boundary. Verify the exact saved PC, status bits, vector read
      order, cycle charge, entry with I set, and return through RTI.
- [x] 4.2 Connect the $2000 NMI enable bit and service pending requests from the facade. Verify enable during
      vblank, one request per rising condition, and that a handler's palette write affects the following frame.
      Run a synthetic NMI wait and a bounded Battle City check. Record the observed stop before choosing
      the next game-facing behavior.
- [x] 4.3 Draw a stationary nametable using the $2000 background pattern table and the $2001 background
      enable bit. Verify asymmetric tiles, both pattern tables, and transparent pattern index zero.
      Run a synthetic cartridge that writes a nametable and confirm that its tiles appear in the startup window.
- [x] 4.4 Apply attribute quadrants. Verify different subpalettes across 16 × 16 regions in a synthetic scene.

## 5. Display sprites and apply rendering modes

- [x] 5.1 Implement $2003/$2004 OAM access. Test consecutive writes, $FF-to-$00 wrapping, and nonincrementing reads.
- [x] 5.2 Implement the $4014 OAM transfer. Test a mirrored CPU page, nonzero start address, and destination wrap.
      Record the omitted DMA stall and rerun Battle City if DMA was the observed obstacle.
- [x] 5.3 Draw 8 × 8 sprites from OAM and CHR. Verify the selected table, position, palette, transparency,
      and pixel placement with an asymmetric synthetic sprite.
- [x] 5.4 Add 8 × 16 sprite selection. Verify both CHR tables and the order of the two tiles.
- [x] 5.5 Compose sprites with the background. Verify OAM ordering, behind-background priority, and all four
      $2001 layer enable combinations. Document whole-frame sprite evaluation in doc/decisions.md.
- [x] 5.6 Apply independent left-edge masks. Verify columns 0 through 7 and the first unmasked column.
- [ ] 5.7 Apply grayscale. Verify that rendering uses the palette code masked with $30.
- [ ] 5.8 Apply the NTSC RGB color emphasis approximation. Verify the three channel selections and document
      the mapping. Run the focused video tests and record the first observed frame or remaining game obstacle.

## 6. Add scrolling and sprite flips

- [ ] 6.1 Add $2005 scrolling and the $2000 base nametable selection. Verify the shared write toggle and both
      nametable boundary crossings. Record the whole-frame scrolling approximation in doc/decisions.md.
- [ ] 6.2 Apply horizontal and vertical sprite flips from OAM. Verify asymmetric sprites in both sizes,
      including the reversed tile order of an 8 × 16 sprite after a vertical flip.
- [ ] 6.3 Replace remaining uses of temporary register-write retention with the corresponding register state, then
      remove `_last_writes` and `last_writes`. Preserve implemented register effects and accept status writes without
      changing vblank or the shared write toggle. Update focused tests and documentation, including the unmodeled
      status-write open-bus effect.
