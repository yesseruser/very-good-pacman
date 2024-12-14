from src.GameObjects.GameBase import GameBase
from src.GameObjects.Ghosts.Ghost import Ghost
from src.Models.GhostMode import GhostMode


class Pink(Ghost):
    def __init__(self, game: GameBase, position: (int, int)):
        super().__init__(game, position, (255, 100, 200))

    def get_target_tile(self) -> (int, int):
        match self.game.get_ghost_mode():
            case GhostMode.CHASE:
                return self.game.get_player_direction().get_moved_position(self.game.get_player_tile(), 4)
            case GhostMode.SCATTER:
                return -1, -1
        return super().get_target_tile()
