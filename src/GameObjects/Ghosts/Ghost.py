import math

import pygame

from src.GameObjects.GameBase import GameBase
from src.GameObjects.MovableGameObject import MovableGameObject
from src.Models.Direction import Direction
from src.Models.GhostMode import GhostMode
from src.Models.LevelTile import solid_tiles


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
        self.direction = Direction.NONE

    def get_target_tile(self) -> (int, int):
        return self.tile_position()

    def get_next_direction(self) -> Direction:
        directions = self.direction.get_possible_ghost_directions()
        distances = {}
        for direction in directions:
            tile = direction.get_moved_position(self.tile_position(), 1)
            if self.game.get_tile_at_tuple(tile) in solid_tiles:
                continue
            distances[direction] = math.dist(tile, self.get_target_tile())

        lowest_distance_pair = sorted(distances.items(), key=lambda x: x[1])[0]
        return lowest_distance_pair[0]

    def update(self):
        mode = self.game.get_ghost_mode()
        if self.last_mode != mode:
            self.direction = self.direction.reversed()
            self.last_mode = mode

        self.next_direction = self.get_next_direction()
        super().update()

    def draw(self):
        pygame.draw.circle(self.game.window, self.color, self.pixel_center_pos, self.game.settings.tile_pixels / 2)
