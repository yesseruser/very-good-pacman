import math

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

    def get_next_direction(self) -> Direction:
        target = self.get_target_tile()
        front = self.direction
        left = Direction.get_relative_direction(self.direction, True)
        right = Direction.get_relative_direction(self.direction, False)
        front_tile = front.get_moved_position(self.tile_position(), 1)
        left_tile = left.get_moved_position(self.tile_position(), 1)
        right_tile = right.get_moved_position(self.tile_position(), 1)
        front_distance = math.dist(front_tile, target)
        left_distance = math.dist(left_tile, target)
        right_distance = math.dist(right_tile, target)

        if front_distance < left_distance and front_distance < right_distance:
            return front
        if left_distance < front_distance and left_distance < right_distance:
            return left
        if right_distance < front_distance and right_distance < left_distance:
            return right

    def update(self):
        mode = self.game.get_ghost_mode()
        if self.last_mode != mode:
            self.direction = self.direction.reversed()
            self.last_mode = mode

        super().update()

    def draw(self):
        pygame.draw.circle(self.game.window, self.color, self.pixel_center_pos, self.game.settings.tile_pixels / 2)
