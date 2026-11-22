"""Verify PPU backdrop rendering from a synthetic CPU program."""

import pygame
import pytest

from frame_display import FrameDisplay
from machine import Machine
from nesfile import NESFile


@pytest.fixture
def display(monkeypatch):
    # The dummy driver lets the presenter expose its scaled pixels without opening a desktop window.
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    pygame.display.quit()
    presenter = FrameDisplay()
    yield presenter
    pygame.display.quit()


@pytest.mark.parametrize("color,rgb", [
    (0x00, (102, 102, 102)),
    (0x01, (0, 42, 136)),
    (0x21, (100, 176, 255)),
    (0x30, (255, 254, 255)),
    (0xE1, (100, 176, 255)),
])
def test_cpu_palette_write_renders_and_presents_backdrop(make_cpu, display, color, rgb):
    # The CPU writes a backdrop color through the PPU's memory-mapped registers.
    program = bytes([
        0xA9,  # LDA #$00: Load zero for PPUMASK.
        0x00,
        0x8D,  # STA $2001: Disable both layers.
        0x01,
        0x20,
        0xA9,  # LDA #$3F: Load the high byte of palette address $3F00.
        0x3F,
        0x8D,  # STA $2006: Set the high byte through PPUADDR.
        0x06,
        0x20,
        0xA9,  # LDA #$00: Load the low byte of palette address $3F00.
        0x00,
        0x8D,  # STA $2006: Set the low byte and select $3F00.
        0x06,
        0x20,
        0xA9,  # LDA #color: Load the test's NES color code.
        color,
        0x8D,  # STA $2007: Write the backdrop color through PPUDATA.
        0x07,
        0x20,
    ])
    cpu, machine = make_cpu(start_address=0x8000, prg_program=program)
    for _ in range(8):
        cpu.step()

    # The native frame uses $3F00 even though the data write advanced the address to $3F01.
    assert machine.ppu.read_vram(0x3F00) == color & 0x3F
    assert machine.ppu._vram_address == 0x3F01
    frame = machine.ppu.render_frame()
    assert frame == bytes(rgb) * (256 * 240)

    # Present the same packed bytes and verify every pixel in the 3× display surface.
    display.present(frame)
    screen = pygame.display.get_surface()
    assert screen.get_size() == (768, 720)
    assert pygame.image.tobytes(screen, "RGB") == bytes(rgb) * (768 * 720)


def test_stationary_background_pattern_tables_and_transparency(tmp_path):
    # Tile 1 has different asymmetric bitplanes in the two pattern tables.
    chr_rom = bytearray(8192)
    chr_rom[16] = 0xA0
    chr_rom[24] = 0x60
    chr_rom[0x1010 + 1] = 0x40
    chr_rom[0x1018 + 1] = 0x80
    prg = bytearray(16384)
    path = tmp_path / "background.nes"
    path.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + prg + chr_rom)
    machine = Machine(NESFile(path))
    ppu = machine.ppu
    for index, code in enumerate((0x0F, 0x01, 0x21, 0x30)):
        ppu.write_vram(0x3F00 + index, code)
    ppu.write_vram(0x2000 + 32 + 2, 1)
    ppu.write_vram(0x23C0, 0xFF)  # Attributes are intentionally deferred.

    def pixel(frame, x, y):
        offset = (y * 256 + x) * 3
        return tuple(frame[offset:offset + 3])

    # Disabled output is all backdrop; enabled output decodes both planes and transparent zero.
    backdrop, first, second, third = (0, 0, 0), (0, 42, 136), (100, 176, 255), (255, 254, 255)
    assert pixel(ppu.render_frame(), 16, 8) == backdrop
    machine.write_byte(0x2009, 0x08)
    frame = ppu.render_frame()
    assert [pixel(frame, x, 8) for x in range(16, 20)] == [first, second, third, backdrop]
    assert pixel(frame, 16, 9) == backdrop
    assert pixel(frame, 15, 8) == backdrop

    # PPUCTRL bit 4 chooses the other table without changing nametable contents.
    machine.write_byte(0x2000, 0x10)
    frame = ppu.render_frame()
    assert [pixel(frame, x, 9) for x in range(16, 19)] == [second, first, backdrop]
    assert pixel(frame, 16, 8) == backdrop

    # A later mirrored PPUMASK write can disable the background again.
    machine.write_byte(0x3FF9, 0xF7)
    assert pixel(ppu.render_frame(), 16, 9) == backdrop
