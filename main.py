import pygame.font

from src.GameObjects.Game import Game
from src.GameObjects.GameSettings import GameSettings


def main():
    pygame.init()
    pygame.font.init()

    game = Game(GameSettings())
    game.loop()


if __name__ == "__main__":
    main()
