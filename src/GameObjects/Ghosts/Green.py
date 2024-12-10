from src.GameObjects.GameBase import GameBase
from src.GameObjects.Ghosts.Ghost import Ghost
from src.Models.GhostMode import GhostMode


class Green(Ghost):
    def __init__(self, game: GameBase, position: (int, int)):
        super().__init__(game, position, (0, 255, 0))

    def get_target_tile(self) -> (int, int):
        match self.game.get_ghost_mode():
            case GhostMode.CHASE:
                return 0, 0
