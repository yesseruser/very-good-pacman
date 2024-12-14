from src.GameObjects.GameBase import GameBase
from src.GameObjects.Ghosts.Ghost import Ghost
from src.Models.GhostMode import GhostMode


class Red(Ghost):
    def __init__(self, game: GameBase, position: (int, int)):
        super().__init__(game, position, (255, 0, 0))
        self.in_ghost_house = False

    def get_target_tile(self) -> (int, int):
        if self.in_ghost_house:
            return self.game.get_ghost_house_exit()

        match self.mode:
            case GhostMode.CHASE:
                return self.game.get_player_tile()
            case GhostMode.SCATTER:
                return self.game.get_level_tile_size()[0] + 1, -1
        return super().get_target_tile()

    def update(self):
        if self.game.has_player_moved():
            self.activated = True

        super().update()