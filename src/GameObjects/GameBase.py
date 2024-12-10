from pygame import SurfaceType

from src.GameObjects.GameSettings import GameSettings
from src.Models.GhostMode import GhostMode
from src.Models.LevelTile import LevelTile


class GameBase:
    settings: GameSettings
    window: SurfaceType
    is_looping: bool

    def get_tile_from_pixel(self, pixel: (int, int)) -> (int, int):
        return (
            int(pixel[0] / self.settings.tile_pixels),
            int(pixel[1] / self.settings.tile_pixels)
        )

    def get_pixel_center_from_tile(self, tile: (int, int)) -> (int, int):
        return (
            int((tile[0] * self.settings.tile_pixels) + (self.settings.tile_pixels / 2)),
            int((tile[1] * self.settings.tile_pixels) + (self.settings.tile_pixels / 2))
        )

    def get_wrapped_position(self, tile: (int, int)) -> (int, int):
        pass

    def get_ghost_mode(self) -> GhostMode:
        pass

    def get_tile_at(self, x: int, y: int) -> LevelTile:
        pass

    def get_tile_at_tuple(self, tile: (int, int)) -> LevelTile:
        return self.get_tile_at(tile[0], tile[1])