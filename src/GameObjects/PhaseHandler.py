import time

from src.GameObjects.GameObject import GameObject
from src.Models.GhostMode import GhostMode


class PhaseHandler(GameObject):
    mode: GhostMode = GhostMode.SCATTER
    start_seconds: float | None = None
    phase: int = 0

    def change_mode(self):
        time_seconds = time.time() - self.start_seconds

        match self.mode:
            case GhostMode.SCATTER:
                if 1 < self.phase < 4 and time_seconds >= 5:
                    self.mode = GhostMode.CHASE
                    self.start_timer()
                elif self.phase <= 1 and time_seconds >= 7:
                    self.mode = GhostMode.CHASE
                    self.start_timer()
            case GhostMode.CHASE:
                if self.phase < 3 and time_seconds >= 20:
                    self.mode = GhostMode.SCATTER
                    self.start_timer()

    def update(self):
        if self.start_seconds is None:
            self.start_timer()

        self.change_mode()

    def start_timer(self):
        self.start_seconds = time.time()