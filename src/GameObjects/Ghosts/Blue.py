from src.GameObjects.GameBase import GameBase
from src.GameObjects.Ghosts.Ghost import Ghost


class Blue(Ghost):
    def __init__(self, game: GameBase, position: (int, int)):
        super().__init__(game, position, (200, 200, 255))
