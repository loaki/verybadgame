from typing import List

import pygame

from project.utils.utils import resource_path


class Images:
    alpha_num: List[pygame.Surface]
    floor: pygame.Surface

    def __init__(self) -> None:
        self.alpha_num = self._load_font(
            path=resource_path("project/assets/fonts/alpha_num.png"), width=20, height=16, total=36, size=1.8
        )
        self.pixel_num = self._load_font(
            path=resource_path("project/assets/fonts/pixel_num.png"), width=10, height=12, total=10, size=2
        )
        self.floor = self._load_texture(path=resource_path("project/assets/floors/floor_1.png"), size=1)
        self.player = self._load_texture(path=resource_path("project/assets/characters/isaac.png"), size=2)

    def _load_font(self, path: str, width: int, height: int, total: int, size: float) -> List[pygame.Surface]:
        surface = pygame.image.load(path)
        digits = [
            pygame.transform.scale(
                surface.subsurface(width * i, 0, width, height), list(map(int, (width * size, height * size)))
            )
            for i in range(total)
        ]
        space = pygame.Surface((width, height)).convert_alpha()
        space.fill((0, 0, 0, 0))
        digits.append(space)
        return digits

    def _load_texture(self, path: str, size: float) -> pygame.Surface:
        surface = pygame.image.load(path)
        return pygame.transform.scale(
            surface, list(map(int, (surface.get_width() * size, surface.get_height() * size)))
        )
