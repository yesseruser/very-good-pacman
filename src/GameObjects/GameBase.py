from pygame import SurfaceType

from src.GameObjects.GameSettings import GameSettings
from src.Models.Direction import Direction
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

    def get_player_tile(self) -> (int, int):
        pass

    def get_player_direction(self) -> Direction:
        pass

    def get_score(self) -> int:
        pass

    def get_coins(self) -> int:
        pass

    def get_lives(self) -> int:
        pass

    def get_tile_at(self, tile: (int, int)) -> LevelTile:
        pass

    def get_level_tile_size(self) -> (int, int):
        pass

    def get_ghost_tile(self, ghost_index: int) -> (int, int):
        pass

    def try_collect_coin(self, tile: (int, int)) -> bool:
        pass

    def try_collect_energizer(self, tile: (int, int)) -> bool:
        pass

    def get_ghost_house_exit(self) -> (int, int):
        pass

    def has_player_moved(self) -> bool:
        pass

    def get_coins_in_level(self) -> int:
        pass