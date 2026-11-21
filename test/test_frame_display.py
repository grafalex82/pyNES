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


def test_fps_uses_presentations_and_elapsed_time(display, monkeypatch):
    # A controllable clock tests the measurement without waiting for real time to pass.
    now = [10.0]
    monkeypatch.setattr("frame_display.monotonic", lambda: now[0])
    display = FrameDisplay()
    frame = bytes((0, 0, 0)) * (256 * 240)
    assert pygame.display.get_caption()[0] == "pyNES - 0.0 FPS"
    display.present(frame)

    # Two frame intervals over 1.5 seconds are averaged; shorter measurements keep the previous title.
    now[0] = 10.5
    display.present(frame)
    now[0] = 10.9
    display.update_fps()
    assert pygame.display.get_caption()[0] == "pyNES - 0.0 FPS"
    now[0] = 11.5
    display.present(frame)
    display.update_fps()
    assert pygame.display.get_caption()[0] == "pyNES - 1.3 FPS"

    # Empty seconds do not reset the measurement, so a frame after five seconds gives 0.2 FPS.
    now[0] = 12.5
    display.update_fps()
    now[0] = 15.5
    display.update_fps()
    assert pygame.display.get_caption()[0] == "pyNES - 1.3 FPS"
    now[0] = 16.5
    display.present(frame)
    display.update_fps()
    assert pygame.display.get_caption()[0] == "pyNES - 0.2 FPS"

    # The same low rate remains correct across the next five-second frame interval.
    now[0] = 21.5
    display.present(frame)
    display.update_fps()
    assert pygame.display.get_caption()[0] == "pyNES - 0.2 FPS"


def test_fps_waits_for_a_presentation_after_a_short_frame_interval(display, monkeypatch):
    # A quick frame alone must not end the measurement when the host subsequently waits several seconds.
    now = [0.0]
    monkeypatch.setattr("frame_display.monotonic", lambda: now[0])
    display = FrameDisplay()
    frame = bytes((0, 0, 0)) * (256 * 240)
    display.present(frame)
    now[0] = 0.1
    display.present(frame)
    now[0] = 4.0
    display.update_fps()
    assert pygame.display.get_caption()[0] == "pyNES - 0.0 FPS"

    # Both frame intervals span five seconds, even though the host checked the title in between.
    now[0] = 5.0
    display.present(frame)
    display.update_fps()
    assert pygame.display.get_caption()[0] == "pyNES - 0.4 FPS"
