import pygame.font

from src.GameObjects.GameBase import GameBase
from src.GameObjects.GameObject import GameObject


class LivesDisplay(GameObject):
    font: pygame.font.Font

    def __init__(self, game: GameBase, pixel_position: (int, int)):
        super().__init__(game, pixel_position)
        self.font = pygame.font.SysFont("monospace", self.game.settings.tile_pixels)

    def draw(self):
        text_surface = self.font.render(f"Lives: {self.game.get_lives()}", False, (255, 255, 255))
        self.game.window.blit(text_surface, self.pixel_center_pos)
