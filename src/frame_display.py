"""Present native-size RGB frames in a pygame window."""

from time import monotonic

import pygame


class FrameDisplay:
    """Scale supplied NES frames to a fixed three-times drawing area."""

    def __init__(self):
        pygame.display.init()
        self._screen = pygame.display.set_mode((768, 720))
        pygame.display.set_caption("pyNES - 0.0 FPS")
        self._fps_started = None
        self._last_presentation_time = None
        self._presented_frames = 0


    def present(self, frame):
        # Integer scaling replicates pixels without blending adjacent colors.
        native = pygame.image.frombytes(frame, (256, 240), "RGB")
        scaled = pygame.transform.scale(native, (768, 720))
        self._screen.blit(scaled, (0, 0))
        pygame.display.flip()

        # The first presentation starts the measurement; later ones complete frame intervals.
        self._last_presentation_time = monotonic()
        if self._fps_started is None:
            self._fps_started = self._last_presentation_time
        else:
            self._presented_frames += 1


    def update_fps(self):
        # End each measurement at a presentation, so waiting between frames remains in the next interval.
        if self._fps_started is not None and self._presented_frames:
            elapsed = self._last_presentation_time - self._fps_started
            if elapsed >= 1:
                pygame.display.set_caption(f"pyNES - {self._presented_frames / elapsed:.1f} FPS")
                self._fps_started = self._last_presentation_time
                self._presented_frames = 0
