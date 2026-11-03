"""
Game state flags telling which screen is active.
"""

from .sound_player import play_sound_assets


class GameState:
    """
    Hold the flags describing the current state of the game.

    Attributes:
        game_running: Whether the main loop must keep running.
        is_paused: Whether the game is paused.
        is_main_menu: Whether the main menu is displayed.
        is_difficulty_select: Whether the difficulty selection screen is
            displayed.
        is_map_selection: Whether the map selection screen is displayed.
        is_in_map: Whether a map is currently displayed.
        is_play_mode: Whether the simulation advances automatically.
    """

    def __init__(self) -> None:
        """
        Initialize the state: the game is running and the main menu is active,
        every other flag is off.
        """
        self.game_running = True
        self.is_paused = False
        self.is_main_menu = True
        self.is_difficulty_select = False
        self.is_map_selection = False
        self.is_in_map = False
        self.is_play_mode = False

    def set_play_mode(self) -> None:
        """
        Toggle the automatic play mode.
        """
        if self.is_play_mode:
            self.is_play_mode = False
        else:
            self.is_play_mode = True

    def set_paused(self) -> None:
        """
        Toggle the paused state.
        """
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True

    def set_main_menu(self) -> None:
        """
        Toggle the main menu state.

        The main menu music is played when the menu becomes active.
        """
        if self.is_main_menu:
            self.is_main_menu = False
        else:
            self.is_main_menu = True
            play_sound_assets(4)

    def set_difficulty_select(self) -> None:
        """
        Toggle the difficulty selection state.

        The main menu music is played when the screen becomes active.
        """
        if self.is_difficulty_select:
            self.is_difficulty_select = False
        else:
            self.is_difficulty_select = True
            play_sound_assets(4)

    def set_map_selector(
        self, current_dif: int, is_change: bool = True
    ) -> None:
        """
        Toggle the map selection state.

        The music matching the current difficulty is played when the screen
        becomes active.

        Args:
            current_dif: Index of the current difficulty, used to pick the
                music.
            is_change: If True, the music is played when the map selection
                becomes active.
        """
        if self.is_map_selection:
            self.is_map_selection = False
        else:
            self.is_map_selection = True
            if is_change:
                play_sound_assets(current_dif)

    def set_in_map(self) -> None:
        """
        Toggle the in-map state.
        """
        if self.is_in_map:
            self.is_in_map = False
        else:
            self.is_in_map = True
