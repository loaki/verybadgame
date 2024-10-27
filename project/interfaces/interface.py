from typing import Optional

import pygame

from project.utils.game_config import GameConfig


class Interface:
    def __init__(
        self,
        config: GameConfig,
        image: Optional[pygame.Surface] = None,
        x: int = 0,
        y: int = 0,
        w: int = 0,
        h: int = 0,
    ) -> None:
        self.config = config
        self.image = image
        self.x = x
        self.y = y
        self.w = w or (image.get_width() if image else 0)
        self.h = h or (image.get_height() if image else 0)

    def update_image(self, image: pygame.Surface, w: int, h: int) -> None:
        self.image = image
        self.w = w or (image.get_width() if image else 0)
        self.h = h or (image.get_height() if image else 0)

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def tick(self) -> None:
        self.draw()

    def draw(self) -> None:
        if self.image:
            self.config.screen.blit(self.image, self.rect)
