class GameState:
    def __init__(self) -> None:
        self.game_running = True
        self.is_paused = False
        self.is_main_menu = True
        self.is_difficulty_select = False
        self.is_map_selection = False

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

    def set_difficulty_select(self) -> None:
        if self.is_difficulty_select:
            self.is_difficulty_select = False
        else:
            self.is_difficulty_select = True

    def set_map_selector(self) -> None:
        if self.is_map_selection:
            self.is_map_selection = False
        else:
            self.is_map_selection = True
