from .sound_player import play_sound_assets


class GameState:
    def __init__(self) -> None:
        self.game_running = True
        self.is_paused = False
        self.is_main_menu = True
        self.is_difficulty_select = False
        self.is_map_selection = False
        self.is_in_map = False
        self.is_play_mode = False

    def set_play_mode(self) -> None:
        if self.is_play_mode:
            self.is_play_mode = False
        else:
            self.is_play_mode = True

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
            play_sound_assets(4)

    def set_difficulty_select(self) -> None:
        if self.is_difficulty_select:
            self.is_difficulty_select = False
        else:
            self.is_difficulty_select = True
            play_sound_assets(4)

    def set_map_selector(self, current_dif: int, is_change: bool = True) -> None:
        if self.is_map_selection:
            self.is_map_selection = False
        else:
            self.is_map_selection = True
            if is_change:
                play_sound_assets(current_dif)

    def set_in_map(self) -> None:
        if self.is_in_map:
            self.is_in_map = False
        else:
            self.is_in_map = True
