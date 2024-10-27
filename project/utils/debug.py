import pygame

from project.utils.game_config import GameConfig


class Debug:
    def __init__(
        self,
        config: GameConfig,
    ) -> None:
        self.config = config

    def draw(self) -> None:
        current_fps = self.config.clock.get_fps()
        font = pygame.font.SysFont("Arial", 13, True)
        fps_text = font.render(f"FPS: {current_fps:.2f}", True, (255, 255, 255))
        self.config.screen.blit(fps_text, (10, 10))
