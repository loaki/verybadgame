import pygame

from project.entities.entity import Entity
from project.utils.game_config import GameConfig


class Player(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config=config)
        self.heads = [config.images.player.subsurface(pygame.Rect((i * 64) * 2, 0, 64, 64)) for i in range(3)]
        self.heads.append(pygame.transform.flip(self.heads[1], True, False))
        self.tearHeads = [config.images.player.subsurface(pygame.Rect(64 + (i * 64) * 2, 0, 64, 64)) for i in range(3)]
        self.tearHeads.append(pygame.transform.flip(self.tearHeads[1], True, False))
        self.feet = [
            [config.images.player.subsurface(pygame.Rect((i * 64), 64, 64, 64)) for i in range(8)],
            [config.images.player.subsurface(pygame.Rect((i * 64), 64 * 2, 64, 64)) for i in range(8)],
            [],
            [],
        ]
        for frame in self.feet[0]:
            self.feet[2].append(frame)
        for frame in self.feet[1]:
            self.feet[3].append(pygame.transform.flip(frame, True, False))

        self.specialFrames = [config.images.player.subsurface(i * 128, 272 + 128, 128, 128) for i in range(1, 3)]
        self.head = self.heads[0]
        self.body = self.feet[0][0]
        self.x = config.window.width // 2
        self.y = config.window.height // 2
        self.direction = "DOWN"
        self.walk = 0
        self.speed = 5

    def move(self, key: str) -> None:
        self.direction = key
        self.walk = (self.walk + 1) % 8
        self.x += ((key == "RIGHT") - (key == "LEFT")) * self.speed
        self.y += ((key == "DOWN") - (key == "UP")) * self.speed

    def update(self) -> None:
        key_map = {
            "DOWN": 0,
            "RIGHT": 1,
            "UP": 2,
            "LEFT": 3,
        }
        self.head = self.heads[key_map[self.direction]]
        self.body = self.feet[key_map[self.direction]][self.walk]

    def draw(self) -> None:
        self.update()
        self.config.screen.blit(self.body, (self.x - 32, self.y - 32))
        self.config.screen.blit(self.head, (self.x - 32, self.y - 32 - 20))
