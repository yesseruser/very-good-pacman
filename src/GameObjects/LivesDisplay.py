import pygame.font

from src.GameObjects.GameBase import GameBase
from src.GameObjects.GameObject import GameObject


class LivesDisplay(GameObject):
    font: pygame.font.Font

    def __init__(self, game: GameBase, pixel_position: (int, int)):
        super().__init__(game, pixel_position)
        self.color = (255, 255, 0)

    def draw(self):
        lives = self.game.get_lives()
        if lives > 0:
            for i in range(lives):
                position = (self.pixel_center_pos[0] + (i * self.game.settings.tile_pixels) + self.game.settings.tile_pixels / 2,
                            self.pixel_center_pos[1] + self.game.settings.tile_pixels / 2)
                pygame.draw.circle(self.game.window, self.color, position,
                                   self.game.settings.tile_pixels / 2)
