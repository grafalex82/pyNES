"""Verify sprite-zero collision timing and its visible eligibility rules."""

import pytest

from machine import Machine
from nesfile import NESFile


def scene(tmp_path, mask=0x1E, x=8, sprite_bits=0x80, background_bits=0xFF, attributes=0):
    # Separate pattern tables make background and sprite transparency independently controllable.
    chr_data = bytearray(8192)
    chr_data[16:24] = bytes([background_bits] * 8)
    chr_data[0x1000:0x1008] = bytes([sprite_bits] * 8)
    path = tmp_path / "hit.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + bytes(16384) + chr_data)
    machine = Machine(NESFile(path))
    for address in range(0x2000, 0x23C0):
        machine.ppu.write_vram(address, 1)
    machine.write_byte(0x2003, 0)
    for value in (0, 0, attributes, x):
        machine.write_byte(0x2004, value)
    machine.write_byte(0x2000, 0x08)
    machine.write_byte(0x2001, mask)
    return machine


def test_hit_timing_lifetime_and_priority(tmp_path):
    # Sprite 0 begins at (8, 1), even when it is behind the opaque background.
    machine = scene(tmp_path, attributes=0x20)
    ppu = machine.ppu
    hit_cycle = (341 + 8 + 3) // 3
    ppu.advance(hit_cycle - 1)
    assert machine.read_byte(0x2002) == 0
    ppu.advance(1)
    assert machine.read_byte(0x200A) == 0x40
    assert machine.read_byte(0x2002) == 0x40
    ppu.advance(27394 - hit_cycle)
    assert machine.read_byte(0x2002) == 0xC0
    assert machine.read_byte(0x2002) == 0x40
    ppu.advance(29667 - 27394)
    assert machine.read_byte(0x2002) == 0


@pytest.mark.parametrize("mask,x,sprite_bits,background_bits", [
    (0x16, 8, 0x80, 0xFF), (0x0E, 8, 0x80, 0xFF),
    (0x1C, 0, 0x80, 0xFF), (0x1A, 0, 0x80, 0xFF),
    (0x1E, 8, 0, 0xFF), (0x1E, 8, 0x80, 0), (0x1E, 255, 0x80, 0xFF),
])
def test_ineligible_pixels_do_not_hit(tmp_path, mask, x, sprite_bits, background_bits):
    machine = scene(tmp_path, mask, x, sprite_bits, background_bits)
    machine.ppu.advance(27394)
    assert machine.read_byte(0x2002) == 0x80


def test_frame_start_sampling_and_repeated_frames(tmp_path):
    # Changes after sampling apply to the next frame, even without host frame output.
    machine = scene(tmp_path)
    machine.ppu.advance(1)
    machine.write_byte(0x2001, 0)
    machine.ppu.advance(27393)
    assert machine.read_byte(0x2002) == 0xC0
    machine.ppu.advance(29781)
    assert machine.read_byte(0x2002) == 0x80


def test_first_eligible_pixel_respects_horizontal_flip(tmp_path):
    # A flipped rightmost source pixel appears at the sprite's left edge.
    machine = scene(tmp_path, x=12, sprite_bits=0x01, attributes=0x40)
    hit_cycle = (341 + 12 + 3) // 3
    machine.ppu.advance(hit_cycle - 1)
    assert machine.read_byte(0x2002) == 0
    machine.ppu.advance(1)
    assert machine.read_byte(0x2002) == 0x40
