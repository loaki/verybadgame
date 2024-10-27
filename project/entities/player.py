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
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.direction = "DOWN"
        self.walk_frame = 0
        self.speed = 5

    def update_vel(self) -> None:
        vel = 0.1
        if sum([self.up, self.down, self.left, self.right]) > 1:
            vel = vel / 1.41421356237
        if self.up:
            self.y_vel = max(self.y_vel - vel, -1)
        if self.down:
            self.y_vel = min(self.y_vel + vel, 1)
        if self.left:
            self.x_vel = max(self.x_vel - vel, -1)
        if self.right:
            self.x_vel = min(self.x_vel + vel, 1)
        if not self.up and not self.down and self.y_vel != 0:
            self.y_vel += vel if self.y_vel < 0 else -vel
        if not self.left and not self.right and self.x_vel != 0:
            self.x_vel += vel if self.x_vel < 0 else -vel
        if self.x_vel < vel and self.x_vel > -vel and self.y_vel < vel and self.y_vel > -vel:
            self.x_vel = 0
            self.y_vel = 0
            self.walk_frame = 0
            self.direction = "DOWN"
        else:
            self.walk_frame = (self.walk_frame + 1) % 8

    def move(self) -> None:
        keys = pygame.key.get_pressed()
        self.up = keys[self.config.controls.up]
        self.down = keys[self.config.controls.down]
        self.left = keys[self.config.controls.left]
        self.right = keys[self.config.controls.right]
        self.direction = (
            "DOWN"
            if self.down
            else "UP" if self.up else "LEFT" if self.left else "RIGHT" if self.right else self.direction
        )

    def update(self) -> None:
        self.move()
        key_map = {
            "DOWN": 0,
            "RIGHT": 1,
            "UP": 2,
            "LEFT": 3,
        }
        self.update_vel()
        self.x += int(self.x_vel * self.speed)
        self.y += int(self.y_vel * self.speed)
        self.head = self.heads[key_map[self.direction]]
        self.body = self.feet[key_map[self.direction]][self.walk_frame]

    def draw(self) -> None:
        self.update()
        self.config.screen.blit(self.body, (self.x - 32, self.y - 32))
        self.config.screen.blit(self.head, (self.x - 32, self.y - 32 - 20))
