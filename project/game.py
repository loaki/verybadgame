import asyncio
import sys

import pygame
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    K_UP,
    KEYDOWN,
    QUIT,
)

from project.entities.floor import Floor
from project.entities.hud import Score
from project.entities.player import Player
from project.utils.controls import Controls
from project.utils.game_config import GameConfig
from project.utils.images import Images
from project.utils.sounds import Sounds
from project.utils.window import Window


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Very Bad Game")
        window = Window(960, 540)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()
        sounds = Sounds()
        controls = Controls()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=sounds,
            controls=controls,
        )

    def check_quit_event(self, event: pygame.event.Event) -> None:
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event: pygame.event.Event) -> bool:
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (event.key in [K_SPACE, K_UP])
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    def player_move_event(self, event: pygame.event.Event) -> str | None:
        keys = pygame.key.get_pressed()
        if keys[self.config.controls.left]:
            return "LEFT"
        elif keys[self.config.controls.right]:
            return "RIGHT"
        elif keys[self.config.controls.up]:
            return "UP"
        elif keys[self.config.controls.down]:
            return "DOWN"
        return None

    async def start(self) -> None:
        while True:
            self.floor = Floor(self.config)
            self.player = Player(self.config)
            self.hud = Score(self.config)
            await self.splash()

    async def splash(self) -> None:
        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return
                if key := self.player_move_event(event):
                    self.player.move(key)

            self.floor.tick()
            self.player.tick()
            self.hud.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()
