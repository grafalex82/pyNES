"""Verify PPU backdrop rendering from a synthetic CPU program."""

import pygame
import pytest

from frame_display import FrameDisplay


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
        0x8D,  # STA $2001: Disable both layers on hardware; layer controls are not implemented yet.
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
