import sys

import pygame.font


class GameSettings:
    tile_pixels = 32
    background_color = (0, 0, 0)
    player_speed = 2
    ghost_speed = 2
    ghost_frightened_speed = 1
    ghost_frightened_color = (0, 100, 255)

    font_tile: pygame.font.Font
    font_200: pygame.font.Font
    font_100: pygame.font.Font

    def __init__(self):
        if hasattr(sys, '_MEIPASS'):
            path = f"{sys._MEIPASS}/res/RobotoMono.ttf"
        else:
            path = f"{sys.path[0]}/res/RobotoMono.ttf"

        self.font_tile = pygame.font.Font(path, int(self.tile_pixels - (self.tile_pixels / 10)))
        self.font_200 = pygame.font.Font(path, 190)
        self.font_100 = pygame.font.Font(path, 90)