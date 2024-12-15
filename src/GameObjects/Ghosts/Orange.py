import math

from src.GameObjects.GameBase import GameBase
from src.GameObjects.Ghosts.Ghost import Ghost
from src.Models.GhostMode import GhostMode


class Orange(Ghost):
    def __init__(self, game: GameBase, position: (int, int)):
        super().__init__(game, position, (255, 100, 0))

    def get_target_tile(self) -> (int, int):
        if self.in_ghost_house:
            return self.game.get_ghost_house_exit()

        match self.mode:
            case GhostMode.CHASE:
                if math.dist(self.game.get_player_tile(), self.tile_position()) > 8:
                    return self.game.get_player_tile()
                return -1, self.game.get_level_tile_size()[1] + 1
            case GhostMode.SCATTER:
                return -1, self.game.get_level_tile_size()[1] + 1
        return super().get_target_tile()

    def update(self):
        if self.game.has_player_moved() and self.game.get_coins() > self.game.get_coins_in_level() / 3:
            self.activated = True
        
        super().update()
