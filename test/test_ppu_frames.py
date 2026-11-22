"""Verify publication of PPU frames at vblank boundaries."""


def test_frame_output_is_optional_and_publishes_each_crossed_vblank(make_cpu):
    # CPU-only use does not construct frames until the host enables frame output.
    _, machine = make_cpu()
    ppu = machine.ppu
    ppu.advance(27394)
    assert ppu.completed_frame is None

    # A large advance publishes each vblank, even when the host has not consumed earlier frames.
    ppu.enable_frame_output()
    ppu.advance(29781 * 3)
    number, frame = ppu.completed_frame
    assert number == 3
    assert frame == bytes((102, 102, 102)) * (256 * 240)


def test_palette_write_between_vblanks_appears_in_the_next_frame(make_cpu):
    # NMI stays disabled while the first color is written to the backdrop palette entry.
    _, machine = make_cpu()
    ppu = machine.ppu
    ppu.enable_frame_output()
    machine.write_byte(0x2000, 0x00)  # PPUCTRL: NMI disabled, increment by 1
    machine.write_byte(0x2006, 0x3F)  # PPUADDR: high byte of $3F00
    machine.write_byte(0x2006, 0x00)  # PPUADDR: low byte of $3F00
    machine.write_byte(0x2007, 0x01)  # PPUDATA: first backdrop color
    ppu.advance(27393)
    assert ppu.completed_frame is None
    ppu.advance(1)
    first = ppu.completed_frame
    assert first == (1, bytes((0, 42, 136)) * (256 * 240))

    # Update the palette after capture; the published first frame must remain unchanged.
    machine.write_byte(0x2006, 0x3F)  # PPUADDR: high byte of $3F00
    machine.write_byte(0x2006, 0x00)  # PPUADDR: low byte of $3F00
    machine.write_byte(0x2007, 0x21)  # PPUDATA: second backdrop color
    assert ppu.completed_frame is first
    ppu.advance(29780)
    assert ppu.completed_frame is first

    # The next vblank publishes the new color, independently of status reads or NMI.
    ppu.advance(1)
    assert ppu.completed_frame == (2, bytes((100, 176, 255)) * (256 * 240))
    assert first == (1, bytes((0, 42, 136)) * (256 * 240))


def test_background_snapshot_tracks_vblank_without_changing_ppu_state(make_cpu):
    # Populate both ends of the nametable and its attributes while the background remains disabled.
    _, machine = make_cpu()
    ppu = machine.ppu
    for address, value in ((0x2000, 0x12), (0x23BF, 0x34), (0x23C0, 0xE4), (0x23FF, 0x1B),
                           (0x3F00, 0x01), (0x3F05, 0x21)):
        ppu.write_vram(address, value)
    machine.write_byte(0x2006, 0x21)
    machine.write_byte(0x2006, 0x23)
    machine.write_byte(0x2006, 0x24)
    state = (ppu._vram_address, ppu._scroll_address_latch, ppu._awaiting_second_write, ppu._vram_read_buffer)
    ppu.enable_frame_output()
    ppu.advance(27393)
    assert ppu.completed_background is None

    # Capturing uses internal VRAM reads, leaving CPU-visible register and latch state untouched.
    ppu.advance(1)
    first = ppu.completed_background
    number, tiles, attributes, colors = first
    assert number == ppu.completed_frame[0] == 1
    assert len(tiles) == 960 and (tiles[0], tiles[-1]) == (0x12, 0x34)
    assert len(attributes) == 64 and (attributes[0], attributes[-1]) == (0xE4, 0x1B)
    assert len(colors) == 16 and (colors[0], colors[5]) == (0x002A88, 0x64B0FF)
    assert (ppu._vram_address, ppu._scroll_address_latch, ppu._awaiting_second_write, ppu._vram_read_buffer) == state

    # Later writes cannot alter the published bytes or palette and only appear at the next vblank.
    ppu.write_vram(0x2000, 0x56)
    ppu.write_vram(0x23C0, 0x39)
    ppu.write_vram(0x3F05, 0x30)
    assert ppu.completed_background is first
    ppu.advance(29781)
    second = ppu.completed_background
    assert second[0] == ppu.completed_frame[0] == 2
    assert (second[1][0], second[2][0], second[3][5]) == (0x56, 0x39, 0xFFFEFF)
    assert (first[1][0], first[2][0], first[3][5]) == (0x12, 0xE4, 0x64B0FF)
