import pygame
from pygame.event import EventType

from src.GameObjects.GameBase import GameBase
from src.GameObjects.GameOverDisplay import GameOverDisplay
from src.GameObjects.GameSettings import GameSettings


class GameOver(GameBase):
    game_over_display: GameOverDisplay
    score: int

    def __init__(self, settings: GameSettings, score: int):
        self.settings = settings
        self.is_looping = False
        self.clock = pygame.time.Clock()
        self.score = score

        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((1100, 300))
        self.game_over_display = GameOverDisplay(self, (0, 0))

    def update(self):
        self.game_over_display.update()

    def on_event(self, event: EventType):
        self.game_over_display.on_event(event)

        if event.type == pygame.QUIT:
            self.is_looping = False

    def draw(self):
        self.window.fill(self.settings.background_color)

        self.game_over_display.draw()

    def loop(self):
        self.is_looping = True
        while self.is_looping:
            self.update()

            for event in pygame.event.get():
                event: EventType
                self.on_event(event)

            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def get_score(self) -> int:
        return self.score
