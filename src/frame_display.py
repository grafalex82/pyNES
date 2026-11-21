"""Present native-size RGB frames in a pygame window."""

import pygame


class FrameDisplay:
    """Scale supplied NES frames to a fixed three-times drawing area."""

    def __init__(self):
        pygame.display.init()
        self._screen = pygame.display.set_mode((768, 720))


    def present(self, frame):
        # Integer scaling replicates pixels without blending adjacent colors.
        native = pygame.image.frombytes(frame, (256, 240), "RGB")
        scaled = pygame.transform.scale(native, (768, 720))
        self._screen.blit(scaled, (0, 0))
        pygame.display.flip()
