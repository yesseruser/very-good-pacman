import pygame
from pygame.event import EventType

from src.GameObjects.GameBase import GameBase
from src.GameObjects.GameSettings import GameSettings
from src.GameObjects.Ghosts.Ghost import Ghost
from src.GameObjects.Ghosts.Orange import Orange
from src.GameObjects.Ghosts.Red import Red
from src.GameObjects.Ghosts.Blue import Blue
from src.GameObjects.Ghosts.Pink import Pink
from src.GameObjects.Level import Level
from src.GameObjects.PhaseHandler import PhaseHandler
from src.GameObjects.Player import Player
from src.Models.Direction import Direction
from src.Models.GhostMode import GhostMode
from src.Models.LevelTile import LevelTile


class Game(GameBase):
    ghosts: list[Ghost]
    player: Player
    level: Level
    phaseHandler: PhaseHandler

    def __init__(self, settings: GameSettings):
        self.settings = settings
        self.is_looping = False
        self.clock = pygame.time.Clock()
        self.phaseHandler = PhaseHandler(self, (0, 0))

        self.level = Level(self)
        self.level.load_from_file("res/level.txt")

        pygame.init()
        self.window = pygame.display.set_mode((len(self.level.map[0]) * settings.tile_pixels,
                                               len(self.level.map) * settings.tile_pixels))

        player_spawn_pixels = self.get_pixel_center_from_tile(self.level.player_spawn)
        self.player = Player(self, player_spawn_pixels)
        self.player.color = (255, 255, 0)
        self.player.speed = settings.player_speed

        self.ghosts = [Red(self, self.get_pixel_center_from_tile(self.level.red_spawn)),
                       Blue(self, self.get_pixel_center_from_tile(self.level.blue_spawn)),
                       Pink(self, self.get_pixel_center_from_tile(self.level.pink_spawn)),
                       Orange(self, self.get_pixel_center_from_tile(self.level.orange_spawn))]

    def update(self):
        self.player.update()
        self.phaseHandler.update()
        for ghost in self.ghosts:
            ghost.update()

    def on_event(self, event: EventType):
        self.player.on_event(event)
        for ghost in self.ghosts:
            ghost.on_event(event)

        if event.type == pygame.QUIT:
            self.is_looping = False

    def draw(self):
        self.window.fill(self.settings.background_color)

        self.level.draw()

        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()

    def loop(self):
        self.is_looping = True
        while self.is_looping:
            self.update()

            for event in pygame.event.get():
                event: EventType
                self.on_event(event)

            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def get_wrapped_position(self, center_pixel: (int, int)) -> (int, int):
        return (
            center_pixel[0] % (self.level.width * self.settings.tile_pixels),
            center_pixel[1] % (self.level.height * self.settings.tile_pixels)
        )

    def get_ghost_mode(self) -> GhostMode:
        return self.phaseHandler.mode

    def get_player_tile(self) -> (int, int):
        return self.player.tile_position()

    def get_player_direction(self) -> Direction:
        return self.player.direction

    def get_score(self) -> int:
        return self.player.score

    def get_lives(self) -> int:
        return self.player.lives

    def get_tile_at(self, x: int, y: int) -> LevelTile:
        if x < 0 or x >= self.level.width or y < 0 or y >= self.level.height:
            return LevelTile.EMPTY

        return self.level.map[y][x]

    def get_level_tile_size(self) -> (int, int):
        return len(self.level.map[0]), len(self.level.map)

    def get_ghost_tile(self, ghost_index: int) -> (int, int):
        return self.ghosts[ghost_index].tile_position()

    def try_collect_coin(self, tile: (int, int)) -> bool:
        if self.get_tile_at_tuple(tile) == LevelTile.COIN:
            self.level.map[tile[1]][tile[0]] = LevelTile.EMPTY
            self.player.on_coin_collected()
            return True
        return False

