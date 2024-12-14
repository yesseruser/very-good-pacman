from src.GameObjects.GameObject import GameObject
from src.GameObjects.Level import Level
from src.Models.Direction import Direction
from src.Models.LevelTile import LevelTile, solid_tiles


class MovableGameObject(GameObject):
    direction: Direction = Direction.NONE
    next_direction: Direction = Direction.NONE
    speed: int

    def move(self):
        if (self.next_direction != Direction.NONE and self.next_direction != self.direction and
            self.game.get_tile_at_tuple(
                self.game.get_tile_from_pixel(
                    self.direction.reversed().get_corner_to_check(self.next_direction,
                                                                  self.pixel_center_pos,
                                                                  self.game.settings.tile_pixels, (-1, 1)))) not in solid_tiles and
            self.game.get_tile_at_tuple(
                self.game.get_tile_from_pixel(
                    self.direction.get_corner_to_check(self.next_direction,
                                                                  self.pixel_center_pos,
                                                                  self.game.settings.tile_pixels,
                                                                  (-1, 1)))) not in solid_tiles):
            self.direction = self.next_direction

        corner1 = self.direction.get_corner_to_check(self.direction.get_relative_direction(),
                                                       self.pixel_center_pos, self.game.settings.tile_pixels, (1, -1))
        corner2 = self.direction.get_corner_to_check(self.direction.get_relative_direction(False),
                                                       self.pixel_center_pos, self.game.settings.tile_pixels, (1, -1))
        tile1 = self.game.get_tile_at_tuple(
                self.game.get_tile_from_pixel(
                    corner1))
        tile2 = self.game.get_tile_at_tuple(
                self.game.get_tile_from_pixel(
                    corner2))

        if tile1 != LevelTile.WALL and tile2 != LevelTile.WALL:
            self.pixel_center_pos = self.game.get_wrapped_position(self.direction.get_moved_position(self.pixel_center_pos, self.speed))

    def update(self):
        self.move()
        super().update()