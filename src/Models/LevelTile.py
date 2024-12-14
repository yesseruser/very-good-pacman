from enum import Enum

class LevelTile(Enum):
    EMPTY = 0
    WALL = 1
    COIN = 2
    ENERGIZER = 3

solid_tiles = [LevelTile.WALL]