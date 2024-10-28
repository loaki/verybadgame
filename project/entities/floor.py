from project.entities.entity import Entity
from project.utils.game_config import GameConfig


class Floor(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(
            config=config, image=config.images.floor, x=0, y=0, w=config.window.width, h=config.window.height
        )

    def draw(self) -> None:
        super().draw()
