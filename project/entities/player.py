import pygame

from project.entities.entity import Entity
from project.utils.common import Common
from project.utils.game_config import GameConfig


class Player(Entity):
    def __init__(self, config: GameConfig, common: Common, x: float, y: float) -> None:
        super().__init__(config=config)
        self.common = common
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
        self.pos_x = x
        self.pos_y = y
        # self.pos_x = float(config.window.width / 2)
        # self.pos_y = float(config.window.height / 2)
        self.vel = 0.4
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.direction = "DOWN"
        self.walk_frame = 0.0
        self.speed = 300.0

    def update_vel(self) -> None:
        vel = self.vel * 30 / (self.common.current_fps or 30)
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
            self.walk_frame = 0.0
            self.direction = "DOWN"
        else:
            self.walk_frame = (self.walk_frame + 30 / (self.common.current_fps or 30)) % 8

    def move(self) -> None:
        if self.common.key_pressed:
            self.up = bool(self.common.key_pressed[self.config.controls.up])
            self.down = bool(self.common.key_pressed[self.config.controls.down])
            self.left = bool(self.common.key_pressed[self.config.controls.left])
            self.right = bool(self.common.key_pressed[self.config.controls.right])
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
        self.pos_x += self.x_vel * self.speed / (self.common.current_fps or 30)
        self.pos_y += self.y_vel * self.speed / (self.common.current_fps or 30)
        self.head = self.heads[key_map[self.direction]]
        self.body = self.feet[key_map[self.direction]][int(self.walk_frame)]

    def draw(self) -> None:
        if (
            int(self.pos_x + 32) > 0
            and int(self.pos_x - 32) < self.config.window.width
            and int(self.pos_y + 32 - 20) > 0
            and int(self.pos_y - 32) < self.config.window.height
        ):
            self.config.screen.blit(self.body, (int(self.pos_x - 32), int(self.pos_y - 32)))
            self.config.screen.blit(self.head, (int(self.pos_x - 32), int(self.pos_y - 32 - 20)))

    def tick(self) -> None:
        self.update()
        return super().tick()
