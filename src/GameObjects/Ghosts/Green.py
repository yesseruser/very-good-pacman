from src.GameObjects.GameBase import GameBase
from src.GameObjects.Ghosts.Ghost import Ghost


class Green(Ghost):
    def __init__(self, game: GameBase, position: (int, int)):
        super().__init__(game, position, (0, 255, 0))
