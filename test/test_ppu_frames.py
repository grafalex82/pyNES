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
