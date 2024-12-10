from src.GameObjects.GameBase import GameBase
from src.GameObjects.Ghosts.Ghost import Ghost


class Red(Ghost):
    def __init__(self, game: GameBase, position: (int, int)):
        super().__init__(game, position, (255, 0, 0))