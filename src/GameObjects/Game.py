import sys

import pygame
from pygame.event import EventType

from src.GameObjects.GameBase import GameBase
from src.GameObjects.GameOver import GameOver
from src.GameObjects.GameSettings import GameSettings
from src.GameObjects.Ghosts.Blue import Blue
from src.GameObjects.Ghosts.Ghost import Ghost
from src.GameObjects.Ghosts.Orange import Orange
from src.GameObjects.Ghosts.Pink import Pink
from src.GameObjects.Ghosts.Red import Red
from src.GameObjects.Level import Level
from src.GameObjects.LivesDisplay import LivesDisplay
from src.GameObjects.PhaseHandler import PhaseHandler
from src.GameObjects.Player import Player
from src.GameObjects.ScoreDisplay import ScoreDisplay
from src.Models.Direction import Direction
from src.Models.GhostMode import GhostMode
from src.Models.LevelTile import LevelTile


class Game(GameBase):
    ghosts: list[Ghost]
    player: Player
    level: Level
    phase_handler: PhaseHandler
    score_display: ScoreDisplay
    lives_display: LivesDisplay

    def __init__(self, settings: GameSettings):
        self.settings = settings
        self.is_looping = False
        self.clock = pygame.time.Clock()
        self.phase_handler = PhaseHandler(self, (0, 0))

        self.level = Level(self)

        if hasattr(sys, '_MEIPASS'):
            self.level.load_from_file(f"{sys._MEIPASS}/res/level.txt")
        else:
            self.level.load_from_file(f"{sys.path[0]}/res/level.txt")

        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((len(self.level.map[0]) * settings.tile_pixels,
                                               len(self.level.map) * settings.tile_pixels))

        player_spawn_pixels = self.get_pixel_center_from_tile(self.level.player_spawn)
        self.player = Player(self, player_spawn_pixels)
        self.player.color = (255, 255, 0)
        self.player.speed = self.settings.player_speed

        self.init_ghosts()

        self.score_display = ScoreDisplay(self, (0, 0))
        self.lives_display = LivesDisplay(self, (0, settings.tile_pixels))

    def init_ghosts(self):
        self.ghosts = [Red(self, self.get_pixel_center_from_tile(self.level.red_spawn)),
                       Blue(self, self.get_pixel_center_from_tile(self.level.blue_spawn)),
                       Pink(self, self.get_pixel_center_from_tile(self.level.pink_spawn)),
                       Orange(self, self.get_pixel_center_from_tile(self.level.orange_spawn))]

    def player_collided(self, ghost: Ghost):
        if ghost.mode != GhostMode.FRIGHTENED:
            self.player.activated = False
            for ghost in self.ghosts:
                ghost.activated = False
                ghost.direction = Direction.NONE

            pygame.time.delay(2000)

            self.player.lives -= 1

            if self.player.lives < 0:
                self.game_over()

            self.player.pixel_center_pos = self.get_pixel_center_from_tile(self.level.player_spawn)
            self.player.direction = Direction.NONE
            self.player.next_direction = Direction.NONE
            self.player.activated = True
            self.init_ghosts()

        elif ghost.mode == GhostMode.FRIGHTENED:
            self.player.score += 200
            self.player.check_extra_life()
            pygame.time.delay(500)
            ghost.pixel_center_pos = ghost.spawn_pixel_position
            ghost.mode = GhostMode.CHASE
            ghost.direction = Direction.NONE
            ghost.in_ghost_house = True

    def update(self):
        self.player.update()
        self.phase_handler.handle_mode_change(self.ghosts)
        for ghost in self.ghosts:
            ghost.update()
            if self.player.tile_position() == ghost.tile_position():
                self.player_collided(ghost)

        self.score_display.update()
        self.lives_display.update()

    def on_event(self, event: EventType):
        self.player.on_event(event)
        for ghost in self.ghosts:
            ghost.on_event(event)
        self.score_display.on_event(event)
        self.lives_display.on_event(event)

        if event.type == pygame.QUIT:
            self.is_looping = False

    def draw(self):
        self.window.fill(self.settings.background_color)

        self.level.draw()

        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()

        self.score_display.draw()
        self.lives_display.draw()

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

    def game_over(self):
        self.is_looping = False
        game_over = GameOver(self.settings, self.player.score)
        game_over.loop()

    def get_wrapped_position(self, center_pixel: (int, int)) -> (int, int):
        return (
            center_pixel[0] % (self.level.width * self.settings.tile_pixels),
            center_pixel[1] % (self.level.height * self.settings.tile_pixels)
        )

    def get_player_tile(self) -> (int, int):
        return self.player.tile_position()

    def get_player_direction(self) -> Direction:
        return self.player.direction

    def get_score(self) -> int:
        return self.player.score

    def get_coins(self) -> int:
        return self.player.coins

    def get_lives(self) -> int:
        return self.player.lives

    def get_tile_at(self, tile: (int, int)) -> LevelTile:
        x = tile[0]
        y = tile[1]
        if x < 0 or x >= self.level.width or y < 0 or y >= self.level.height:
            return LevelTile.EMPTY

        return self.level.map[y][x]

    def get_level_tile_size(self) -> (int, int):
        return len(self.level.map[0]), len(self.level.map)

    def get_ghost_tile(self, ghost_index: int) -> (int, int):
        return self.ghosts[ghost_index].tile_position()

    def try_collect_coin(self, tile: (int, int)) -> bool:
        if self.get_tile_at(tile) == LevelTile.COIN:
            self.level.map[tile[1]][tile[0]] = LevelTile.EMPTY
            self.player.on_coin_collected()
            return True
        return False

    def try_collect_energizer(self, tile: (int, int)) -> bool:
        if self.get_tile_at(tile) == LevelTile.ENERGIZER:
            self.level.map[tile[1]][tile[0]] = LevelTile.EMPTY
            self.phase_handler.frighten_ghosts(self.ghosts)
            self.player.on_energizer_collected()
            return True
        return False

    def get_ghost_house_exit(self) -> (int, int):
        return self.level.red_spawn

    def has_player_moved(self) -> bool:
        return self.player.direction != Direction.NONE

    def get_coins_in_level(self) -> int:
        return self.level.coin_amount
