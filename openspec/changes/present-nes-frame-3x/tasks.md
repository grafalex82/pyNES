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
- [ ] 2.4 Give $2006 its two-write address effect and reset the write toggle on $2002 reads. Test interrupted
      pairs and register aliases. Update doc/memory.md as the register effects replace the retained-write stub.
- [ ] 2.5 Implement writes to $2007. Verify successive stores with both increments selected by $2000 bit 2.
- [ ] 2.6 Render the backdrop from $3F00. Run a synthetic CPU program that writes the palette through Machine
      and show the resulting color using the stage 1 presenter. Assert its native and scaled RGB output in pytest.
- [ ] 2.7 Add buffered reads from $2007. Verify CHR and nametable priming, immediate palette reads, the palette
      read's buffer refill, and increment behavior through register mirrors.

## 3. Display the background

- [ ] 3.1 Draw a stationary nametable using the $2000 background pattern table and the $2001 background
      enable bit. Verify asymmetric tiles, both pattern tables, and transparent pattern index zero.
- [ ] 3.2 Apply attribute quadrants. Verify different subpalettes across 16 × 16 regions in a synthetic scene.
- [ ] 3.3 Add $2005 scrolling and the $2000 base nametable selection. Verify the shared write toggle and both
      nametable boundary crossings. Record the whole-frame scrolling approximation in doc/decisions.md.

## 4. Advance video and present emulated frames

- [ ] 4.1 Advance the PPU by completed CPU cycles and derive $2002 bit 7 from the frame phase. Test status
      clearing, recurring vblank without polling, and zero-cycle runs. Document the timing and status approximation.
- [ ] 4.2 Add CPU NMI entry at an instruction boundary. Verify the exact saved PC, status bits, vector read
      order, cycle charge, entry with I set, and return through RTI.
- [ ] 4.3 Connect the $2000 NMI enable bit and service pending requests from the facade. Verify enable during
      vblank and one request per rising condition. Run a synthetic NMI wait and a bounded Battle City check.
      Record the observed stop before choosing the next game-facing behavior.
- [ ] 4.4 Publish a completed frame at vblank entry. Verify that an NMI handler's palette update is visible
      in the following completed frame.
- [ ] 4.5 Open the display before the first CPU block when running `python main.py ROM`. With a synthetic
      cartridge, verify startup order, frame presentation, close events, and failure cleanup with traceback
      propagation. Verify that `--help` leaves the display uninitialized. Document the command in README.md.

## 5. Display sprites and apply rendering modes

- [ ] 5.1 Implement $2003/$2004 OAM access. Test consecutive writes, $FF-to-$00 wrapping, and nonincrementing reads.
- [ ] 5.2 Implement the $4014 OAM transfer. Test a mirrored CPU page, nonzero start address, and destination wrap.
      Record the omitted DMA stall and rerun Battle City if DMA was the observed obstacle.
- [ ] 5.3 Draw 8 × 8 sprites from OAM and CHR. Verify the selected table, position, palette, transparency,
      and both flips with an asymmetric synthetic sprite.
- [ ] 5.4 Add 8 × 16 sprite selection. Verify both CHR tables and tile order before and after a vertical flip.
- [ ] 5.5 Compose sprites with the background. Verify OAM ordering, behind-background priority, and all four
      $2001 layer enable combinations. Document whole-frame sprite evaluation in doc/decisions.md.
- [ ] 5.6 Apply independent left-edge masks. Verify columns 0 through 7 and the first unmasked column.
- [ ] 5.7 Apply grayscale. Verify that rendering uses the palette code masked with $30.
- [ ] 5.8 Apply the NTSC RGB color emphasis approximation. Verify the three channel selections and document
      the mapping. Run the focused video tests and record the first observed frame or remaining game obstacle.
