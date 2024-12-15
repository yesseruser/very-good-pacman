import math

import pygame.draw
from pygame.event import EventType

from src.GameObjects.GameBase import GameBase
from src.GameObjects.MovableGameObject import MovableGameObject
from src.Models.Direction import Direction


class Player(MovableGameObject):
    lives: int
    score: int
    coins: int
    awarded_extra_lives: int

    def __init__(self, game: GameBase, pixel_position: (int, int)):
        super().__init__(game, pixel_position)
        self.lives = 2
        self.score = 0
        self.coins = 0
        self.awarded_extra_lives = 0
        self.activated = True

    def draw(self):
        pygame.draw.circle(self.game.window, self.color, self.pixel_center_pos, self.game.settings.tile_pixels / 2)

    def on_event(self, event: EventType):
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                self.next_direction = Direction.UP
            elif pressed[pygame.K_DOWN]:
                self.next_direction = Direction.DOWN
            elif pressed[pygame.K_LEFT]:
                self.next_direction = Direction.LEFT
            elif pressed[pygame.K_RIGHT]:
                self.next_direction = Direction.RIGHT

    def update(self):
        super().update()
        self.game.try_collect_coin(self.tile_position())
        self.game.try_collect_energizer(self.tile_position())

    def on_coin_collected(self):
        self.coins += 1
        self.score += 10
        self.check_extra_life()

    def on_energizer_collected(self):
        self.score += 50
        self.check_extra_life()

    def check_extra_life(self):
        cropped_score = self.score - (self.awarded_extra_lives * 1000)
        extra_lives = math.floor(cropped_score / 1000)
        self.lives += extra_lives
        self.awarded_extra_lives += extra_lives
