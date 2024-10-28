import pygame

from project.interfaces.interface import Interface
from project.utils.common import Common
from project.utils.game_config import GameConfig


class Score(Interface):
    def __init__(self, config: GameConfig, common: Common) -> None:
        super().__init__(config=config)
        self.common = common
        self.y = int(self.config.window.height * 0.1)
        self.score = 0

    def reset(self) -> None:
        self.score = 0

    def add(self) -> None:
        self.score += 1
        self.config.sounds.point.play()

    @property
    def rect(self) -> pygame.Rect:
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.pixel_num[digit] for digit in score_digits]
        w = sum(image.get_width() for image in images)
        x = (self.config.window.width - w) / 2
        h = max(image.get_height() for image in images)
        return pygame.Rect(x, self.y, w, h)

    def draw(self, surface: pygame.Surface) -> None:
        if self.common.key_pressed and self.common.key_pressed[self.config.controls.space]:
            self.add()
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.pixel_num[digit] for digit in score_digits]
        digits_width = sum(image.get_width() for image in images)
        x_offset = (self.config.window.width - digits_width) / 2

        for image in images:
            surface.blit(image, (x_offset, self.y))
            x_offset += image.get_width()
