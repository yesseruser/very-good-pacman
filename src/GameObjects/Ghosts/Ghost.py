import math

import pygame

from src.GameObjects.GameBase import GameBase
from src.GameObjects.MovableGameObject import MovableGameObject
from src.Models.Direction import Direction
from src.Models.GhostMode import GhostMode
from src.Models.LevelTile import LevelTile


class Ghost(MovableGameObject):
    last_mode: GhostMode
    last_tile: (int, int)

    def __init__(self, game: GameBase, position: (int, int), color: (int, int, int)):
        super().__init__(game, position)
        self.color = color
        self.speed = 4
        self.phase = 0
        self.last_mode = game.get_ghost_mode()
        self.last_tile = position
        self.direction = Direction.UP

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
        distances = {
            front: math.dist(front_tile, target),
            left: math.dist(left_tile, target),
            right: math.dist(right_tile, target)
        }

        valid_dirs = []

        if self.game.get_tile_at_tuple(front_tile) != LevelTile.WALL:
            valid_dirs.append(front)
        if self.game.get_tile_at_tuple(left_tile) != LevelTile.WALL:
            valid_dirs.append(left)
        if self.game.get_tile_at_tuple(right_tile) != LevelTile.WALL:
            valid_dirs.append(right)

        min_dir = valid_dirs[0]

        for i in valid_dirs:
            for direction in valid_dirs:
                if distances[direction] < distances[min_dir]:
                    min_dir = direction

        return min_dir


    def update(self):
        mode = self.game.get_ghost_mode()
        if self.last_mode != mode:
            self.direction = self.direction.reversed()
            self.last_mode = mode

        if self.tile_position() != self.last_tile:
            self.get_next_direction()
        super().update()

    def draw(self):
        pygame.draw.circle(self.game.window, self.color, self.pixel_center_pos, self.game.settings.tile_pixels / 2)
