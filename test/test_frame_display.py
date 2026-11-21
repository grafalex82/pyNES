"""Tests for presenting supplied RGB frames."""

import pygame
import pytest

from frame_display import FrameDisplay


@pytest.fixture
def display(monkeypatch):
    # The dummy driver exposes the display surface without opening a desktop window.
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    pygame.display.quit()
    presenter = FrameDisplay()
    yield presenter
    pygame.display.quit()


def test_present_scales_every_pixel_to_a_three_by_three_block(display):
    # Vary all color channels across rows and columns, including the last pixel.
    rows = [bytes(channel for x in range(256) for channel in (x, y, (x + y) % 256)) for y in range(240)]
    display.present(b"".join(rows))

    # Construct the expected image independently by repeating RGB triples and rows.
    scaled_rows = [b"".join(row[x:x + 3] * 3 for x in range(0, len(row), 3)) for row in rows]
    expected = b"".join(row * 3 for row in scaled_rows)
    screen = pygame.display.get_surface()
    assert screen.get_size() == (768, 720)
    assert pygame.image.tobytes(screen, "RGB") == expected


def test_present_reuses_window_and_replaces_previous_frame(display):
    # Distinct solid frames make any pixel left from the previous presentation visible.
    first_color = bytes((230, 20, 70))
    second_color = bytes((10, 180, 240))
    display.present(first_color * (256 * 240))
    screen = pygame.display.get_surface()
    assert pygame.image.tobytes(screen, "RGB") == first_color * (768 * 720)

    # The display surface stays the same while all of its pixels take the new color.
    display.present(second_color * (256 * 240))
    assert pygame.display.get_surface() is screen
    assert pygame.image.tobytes(screen, "RGB") == second_color * (768 * 720)
