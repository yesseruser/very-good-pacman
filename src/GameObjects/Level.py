import pygame.draw
from pygame.rect import RectType

from src.GameObjects.GameBase import GameBase
from src.Models.LevelTile import LevelTile


def character_to_tile(character: str) -> LevelTile:
    match character:
        case " ":
            return LevelTile.EMPTY
        case "Z":
            return LevelTile.WALL
        case ".":
            return LevelTile.COIN

    return LevelTile.EMPTY


class Level:
    height: int
    width: int
    map: list[list[LevelTile]]
    is_loaded: bool
    game: GameBase

    def __init__(self, game: GameBase):
        self.map = []
        self.width = 0
        self.height = 0
        self.player_spawn = (0, 0)
        self.game = game
        self.is_loaded = False

    def load_from_file(self, filename: str):
        with open(filename, "r") as file:
            lines = file.read().split("\n")
            self.map = []
            for line in lines:
                row = []
                for character in line:
                    if character == "P":
                        self.player_spawn = (len(row), len(self.map))
                        row.append(LevelTile.EMPTY)
                        continue
                    row.append(character_to_tile(character))
                self.map.append(row)

        self.height = len(self.map)
        self.width = len(self.map[0])
        self.is_loaded = True

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                match self.map[y][x]:
                    case LevelTile.WALL:
                        self.draw_wall(x, y)
                    case LevelTile.COIN:
                        self.draw_coin(x, y)

    def draw_wall(self, x: int, y: int):
        pixel_center = self.game.get_pixel_center_from_tile((x, y))

        pygame.draw.rect(self.game.window, (0, 0, 150),
                         (pixel_center[0] - (self.game.settings.tile_pixels / 2), pixel_center[1] - (self.game.settings.tile_pixels / 2),
                            self.game.settings.tile_pixels, self.game.settings.tile_pixels))

    def draw_coin(self, x: int, y: int):
        pygame.draw.circle(self.game.window, (235, 230, 0),
                           self.game.get_pixel_center_from_tile((x, y)), self.game.settings.tile_pixels / 10)
