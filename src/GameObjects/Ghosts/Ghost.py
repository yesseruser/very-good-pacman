import math
import random

import pygame

from src.GameObjects.GameBase import GameBase
from src.GameObjects.MovableGameObject import MovableGameObject
from src.Models.Direction import Direction
from src.Models.GhostMode import GhostMode
from src.Models.LevelTile import solid_tiles, LevelTile


class Ghost(MovableGameObject):
    mode: GhostMode
    last_mode: GhostMode
    last_tile: (int, int)
    in_ghost_house: bool
    spawn_pixel_position: (int, int)
    base_color: (int, int, int)

    def __init__(self, game: GameBase, position: (int, int), color: (int, int, int)):
        super().__init__(game, position)
        self.color = color
        self.base_color = color
        self.speed = game.settings.ghost_speed
        self.phase = 0
        self.last_tile = position
        self.direction = Direction.NONE
        self.in_ghost_house = True
        self.activated = False
        self.spawn_pixel_position = position
        self.last_mode = GhostMode.CHASE
        self.mode = GhostMode.CHASE

    def get_target_tile(self) -> (int, int):
        if self.in_ghost_house:
            return self.game.get_ghost_house_exit()
        return self.tile_position()

    def get_solid_tiles(self) -> list[LevelTile]:
        if self.in_ghost_house:
            tiles = solid_tiles.copy()
            tiles = list(filter(lambda x: x != LevelTile.GHOST_HOUSE, tiles))
            return tiles

        return solid_tiles

    def get_next_direction(self) -> Direction:
        directions = self.direction.get_possible_ghost_directions()

        distances = {}
        for direction in directions:
            tile = direction.get_moved_position(self.tile_position(), 1)
            if self.game.get_tile_at(tile) in self.get_solid_tiles():
                continue
            distances[direction] = math.dist(tile, self.get_target_tile())

        if self.mode == GhostMode.FRIGHTENED and not self.in_ghost_house:
            return random.choice(list(distances.keys()))

        filtered = filter(lambda x: True, distances.items())
        if self.game.get_tile_at(self.tile_position()) == LevelTile.NO_VERTICAL:
            filtered = filter(lambda x: x[0] != Direction.UP and x[0] != Direction.DOWN, distances.items())

        lowest_distance_pair = sorted(filtered, key=lambda x: x[1])[0]
        return lowest_distance_pair[0]

    def update(self):
        mode = self.mode
        if self.last_mode != mode and self.mode != GhostMode.FRIGHTENED:
            self.direction = self.direction.reversed()
            self.last_mode = mode

        if self.mode != GhostMode.FRIGHTENED:
            self.color = self.base_color
            self.speed = self.game.settings.ghost_speed

        if self.mode == GhostMode.FRIGHTENED:
            self.color = self.game.settings.ghost_frightened_color
            self.speed = self.game.settings.ghost_frightened_speed

        if self.last_tile != self.tile_position():
            self.next_direction = self.get_next_direction()
            self.last_tile = self.tile_position()

        if self.tile_position() == self.game.get_ghost_house_exit():
            self.in_ghost_house = False
        super().update()

    def draw(self):
        pygame.draw.circle(self.game.window, self.color, self.pixel_center_pos, self.game.settings.tile_pixels / 2)
