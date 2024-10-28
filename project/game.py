import asyncio
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List

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
        window = Window(1920, 1080)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()
        sounds = Sounds()
        controls = Controls()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=120,
            window=window,
            images=images,
            sounds=sounds,
            controls=controls,
        )
        self.combined_surface = pygame.Surface((self.config.window.width, self.config.window.height), pygame.SRCALPHA)
        if self.config.workers > 0:
            self.executor = ThreadPoolExecutor(max_workers=self.config.workers)

    def check_quit_event(self, event: pygame.event.Event) -> None:
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    def update_entities(self, entities: List[Player]) -> None:
        for entity in entities:
            entity.update()

    def draw_entities(self, entities: List[Player], surface: pygame.Surface) -> None:
        for entity in entities:
            entity.draw(surface)

    def tick_entities(self, entities: List[Player], surface: pygame.Surface) -> None:
        for entity in entities:
            entity.tick(surface)

    async def start(self) -> None:
        while True:
            self.common = Common(self.config)
            self.debug = Debug(self.config)

            self.floor = Floor(self.config)
            # self.player = Player(self.config, self.common)
            self.players = [
                Player(self.config, self.common, x * 64, y * 64) for x in range(0, 50) for y in range(-50, 50)
            ]
            self.hud = Score(self.config, self.common)
            self.entities = []
            for player in self.players:
                self.entities.append(player)
            await self.splash()

    async def splash(self) -> None:
        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)

            self.floor.tick(self.combined_surface)

            if self.config.workers > 0:
                tasks = [
                    asyncio.get_running_loop().run_in_executor(
                        self.executor,
                        self.update_entities,
                        self.entities[
                            worker
                            * len(self.entities)
                            // self.config.workers : (worker + 1)
                            * len(self.entities)
                            // self.config.workers
                        ],
                    )
                    for worker in range(self.config.workers)
                ]
                await asyncio.gather(*tasks)
                self.draw_entities(self.entities, self.combined_surface)
            else:
                self.tick_entities(self.entities, self.combined_surface)

            self.hud.tick(self.combined_surface)
            if self.config.debug:
                self.debug.tick(self.combined_surface)

            self.config.screen.blit(self.combined_surface, (0, 0))

            self.common.update()
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()


if __name__ == "__main__":
    asyncio.run(Game().start())
