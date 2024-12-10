# 4,3,3-triethyl-2,5-dipropyldekan

from pygame.event import EventType

from src.GameObjects.GameBase import GameBase


class GameObject:
    game: GameBase
    pixel_center_pos: (int, int)
    size: int
    color: (int, int, int)

    def __init__(self, game: GameBase, pixel_position: (int, int)):
        self.game = game
        self.color = (255, 255, 255)
        self.pixel_center_pos = pixel_position

    def draw(self):
        pass

    def update(self):
        pass

    def on_event(self, event: EventType):
        pass

    def tile_position(self):
        return self.game.get_tile_from_pixel(self.pixel_center_pos)