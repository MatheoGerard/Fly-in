class GameState:
    def __init__(self) -> None:
        self.game_running = True
        self.is_paused = False
        self.is_main_menu = True

    def set_paused(self) -> None:
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True

    def set_main_menu(self) -> None:
        if self.is_main_menu:
            self.is_main_menu = False
        else:
            self.is_main_menu = True
