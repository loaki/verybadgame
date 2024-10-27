import pygame

from project.utils.game_config import GameConfig


class Common:
    def __init__(
        self,
        config: GameConfig,
    ) -> None:
        self.config = config
        self.current_fps = 0.0
        self.key_pressed = pygame.key.ScancodeWrapper()

    def update(self) -> None:
        self.current_fps = self.config.clock.get_fps()
        self.key_pressed = pygame.key.get_pressed()
