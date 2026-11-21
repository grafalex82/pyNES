"""Present native-size RGB frames in a pygame window."""

from time import monotonic

import pygame


class FrameDisplay:
    """Scale supplied NES frames to a fixed three-times drawing area."""

    def __init__(self):
        pygame.display.init()
        self._screen = pygame.display.set_mode((768, 720))
        pygame.display.set_caption("pyNES - 0.0 FPS")
        self._fps_started = monotonic()
        self._presented_frames = 0


    def present(self, frame):
        # Integer scaling replicates pixels without blending adjacent colors.
        native = pygame.image.frombytes(frame, (256, 240), "RGB")
        scaled = pygame.transform.scale(native, (768, 720))
        self._screen.blit(scaled, (0, 0))
        pygame.display.flip()
        self._presented_frames += 1


    def update_fps(self):
        # Measure actual presentations over wall-clock time, independent of emulated frame timing.
        now = monotonic()
        elapsed = now - self._fps_started
        if elapsed >= 1:
            pygame.display.set_caption(f"pyNES - {self._presented_frames / elapsed:.1f} FPS")
            self._fps_started = now
            self._presented_frames = 0
