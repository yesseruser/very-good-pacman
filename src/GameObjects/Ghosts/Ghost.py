import pygame

from src.GameObjects.GameBase import GameBase
from src.GameObjects.MovableGameObject import MovableGameObject
from src.Models.Direction import Direction
from src.Models.GhostMode import GhostMode


class Ghost(MovableGameObject):
    last_mode: GhostMode

    def __init__(self, game: GameBase, position: (int, int), color: (int, int, int)):
        super().__init__(game, position)
        self.color = color
        self.speed = 10
        self.phase = 0
        self.last_mode = game.get_ghost_mode()
        self.direction = Direction.NONE

    def get_target_tile(self) -> (int, int):
        return self.tile_position()

    def update(self):
        mode = self.game.get_ghost_mode()
        if self.last_mode != mode:
            self.direction = self.direction.reversed()
            self.last_mode = mode

    def draw(self):
        pygame.draw.circle(self.game.window, self.color, self.pixel_center_pos, self.game.settings.tile_pixels / 2)
