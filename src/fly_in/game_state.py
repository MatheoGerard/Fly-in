class GameState:
    def __init__(self) -> None:
        self.game_running = True
        self.is_paused = False

    def set_paused(self) -> None:
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True
