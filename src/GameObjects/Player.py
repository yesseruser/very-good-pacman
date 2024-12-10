import pygame.draw
from pygame.event import EventType

from src.GameObjects.MovableGameObject import MovableGameObject
from src.Models.Direction import Direction


class Player(MovableGameObject):
    lives: int
    points: int

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
