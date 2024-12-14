from enum import Enum

class LevelTile(Enum):
    EMPTY = 0
    WALL = 1
    COIN = 2
    ENERGIZER = 3
    GHOST_HOUSE = 4
    NO_VERTICAL = 5

solid_tiles = [LevelTile.WALL, LevelTile.GHOST_HOUSE]