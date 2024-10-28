import sys

import pygame

from project.utils.utils import resource_path


class Sounds:
    die: pygame.mixer.Sound
    hit: pygame.mixer.Sound
    point: pygame.mixer.Sound
    swoosh: pygame.mixer.Sound
    wing: pygame.mixer.Sound

    def __init__(self) -> None:
        if "win" in sys.platform:
            ext = "wav"
        else:
            ext = "ogg"
        self.point = pygame.mixer.Sound(resource_path(f"project/assets/audio/point.{ext}"))
