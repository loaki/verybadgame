import os

import pygame

from project.utils.controls import Controls
from project.utils.images import Images
from project.utils.sounds import Sounds
from project.utils.window import Window


class GameConfig:
    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        fps: int,
        window: Window,
        images: Images,
        sounds: Sounds,
        controls: Controls,
    ) -> None:
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.window = window
        self.images = images
        self.sounds = sounds
        self.controls = controls
        self.debug = os.environ.get("DEBUG", False)

    def tick(self) -> None:
        self.clock.tick(self.fps)
