from src.GameObjects.GameBase import GameBase
from src.GameObjects.Ghosts.Ghost import Ghost
from src.Models.GhostMode import GhostMode


class Blue(Ghost):
    def __init__(self, game: GameBase, position: (int, int)):
        super().__init__(game, position, (0, 255, 255))

    def get_target_tile(self) -> (int, int):
        if self.in_ghost_house:
            return self.game.get_ghost_house_exit()

        match self.game.get_ghost_mode():
            case GhostMode.CHASE:
                center_point = self.game.get_pixel_center_from_tile(self.game.get_player_direction().get_moved_position(
                    self.game.get_player_tile(), 2))
                start_point = self.game.get_pixel_center_from_tile(self.game.get_ghost_tile(0))
                direction_vector = (center_point[0] - start_point[0], center_point[1] - start_point[1])
                scaled_direction_vector = (2 * direction_vector[0], 2 * direction_vector[1])
                end_point = (start_point[0] + scaled_direction_vector[0], start_point[1] + scaled_direction_vector[1])
                end_tile = self.game.get_tile_from_pixel(end_point)
                return end_tile
            case GhostMode.SCATTER:
                return self.game.get_level_tile_size()[0] + 1, self.game.get_level_tile_size()[1] + 1
        return super().get_target_tile()
