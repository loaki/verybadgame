import asyncio
import sys

import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from project.entities.floor import Floor
from project.entities.player import Player
from project.interfaces.score import Score
from project.utils.common import Common
from project.utils.controls import Controls
from project.utils.debug import Debug
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
            fps=60,
            window=window,
            images=images,
            sounds=sounds,
            controls=controls,
        )

    def check_quit_event(self, event: pygame.event.Event) -> None:
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    async def start(self) -> None:
        while True:
            self.common = Common(self.config)
            self.debug = Debug(self.config)

            self.floor = Floor(self.config)
            self.player = Player(self.config, self.common)
            self.hud = Score(self.config, self.common)
            await self.splash()

    async def splash(self) -> None:
        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)

            self.floor.tick()
            self.player.tick()
            self.hud.tick()

            if self.config.debug:
                self.debug.draw()

            self.common.update()
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()
