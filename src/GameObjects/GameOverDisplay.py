import pygame.font

from src.GameObjects.GameBase import GameBase
from src.GameObjects.GameObject import GameObject
from src.Models.Direction import Direction


class GameOverDisplay(GameObject):
    font: pygame.font.Font

    def __init__(self, game: GameBase, pixel_position: (int, int)):
        super().__init__(game, pixel_position)
        self.font = self.game.settings.font_200
        self.score_font = self.game.settings.font_100

    def draw(self):
        text_surface = self.font.render("Game Over", False, (255, 255, 255))
        self.game.window.blit(text_surface, self.pixel_center_pos)
        score_surface = self.score_font.render(f"Score: {self.game.get_score()}", False, (255, 255, 255))
        self.game.window.blit(score_surface, Direction.DOWN.get_moved_position(self.pixel_center_pos, 200))

