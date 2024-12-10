import math
from enum import Enum
from operator import truediv


class Direction(Enum):
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def reversed(self):
        match self:
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP

        return Direction.NONE

    def get_moved_position(self, position: (int, int), modifier: int = 1) -> (int, int):
        match self:
            case Direction.UP:
                return position[0], position[1] - modifier
            case Direction.DOWN:
                return position[0], position[1] + modifier
            case Direction.LEFT:
                return position[0] - modifier, position[1]
            case Direction.RIGHT:
                return position[0] + modifier, position[1]

        return position

    def get_corner_to_check(self, other, position: (int, int), size: int, offset: (int, int) = (0, 0)) -> (int, int):
        if self == Direction.NONE or other == Direction.NONE or other == self or other == self.reversed():
            return position

        position = self.get_moved_position(position, math.floor(size / 2) + offset[0])
        position = other.get_moved_position(position, math.floor(size / 2) + offset[1])
        return position

    def get_relative_direction(self, counterclockwise: bool = True):
        match self:
            case Direction.RIGHT:
                return Direction.UP if counterclockwise else Direction.DOWN
            case Direction.LEFT:
                return Direction.DOWN if counterclockwise else Direction.UP
            case Direction.UP:
                return Direction.LEFT if counterclockwise else Direction.RIGHT
            case Direction.DOWN:
                return Direction.RIGHT if counterclockwise else Direction.LEFT

        return Direction.NONE
