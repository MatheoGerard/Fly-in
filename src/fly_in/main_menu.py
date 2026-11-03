"""
Main menu, difficulty selection and map selection.
"""

import pygame as pg
from .game_state import GameState


class Button:
    """
    Button of the main menu.

    Attributes:
        is_selected: Whether the button is selected.
        text: Text of the button.
        position: Position ``[x, y]`` of the button on screen.
        dim: Dimensions ``[width, height]`` of the button.
    """

    def __init__(
        self, selected: bool, text_in_button: str, x: int, y: int
    ) -> None:
        """
        Initialize the button.

        Args:
            selected: Whether the button starts selected.
            text_in_button: Text of the button.
            x: Horizontal position of the button.
            y: Vertical position of the button.
        """
        self.is_selected: bool = selected
        self.text: str = text_in_button
        self.position: list[int] = [x, y]
        self.dim: list[int] = [600, 150]


class MainMenu:
    """
    Main menu of the game.

    Attributes:
        nb_options: Number of buttons of the menu.
        selection_state: Index of the selected button.
        background: Background image of the menu.
        buttons: Buttons of the menu.
        first_but_position: Position ``[x, y]`` of the next button to create.
    """

    def __init__(
        self, background_path: str, game_manager: GameState, options: int
    ) -> None:
        """
        Initialize the menu and load its background.

        Args:
            background_path: Path of the background image.
            game_manager: State of the game.
            options: Number of buttons of the menu.
        """
        self.nb_options: int = options
        self.selection_state: int = 0
        self.background: pg.surface.Surface = pg.image.load(background_path)
        self.buttons: list[Button] = []
        self.first_but_position: list[int] = [1075, 690]

    def create_button(self) -> None:
        """
        Create the buttons of the menu.

        The first button is PLAY and is selected, the other ones are QUIT
        buttons. They are stacked vertically, 150 pixels apart.
        """
        self.buttons.append(
            Button(
                True,
                "PLAY",
                self.first_but_position[0],
                self.first_but_position[1],
            ),
        )

        self.first_but_position[1] += 150

        for _ in range(0, self.nb_options - 1):
            self.buttons.append(
                Button(
                    False,
                    "QUIT",
                    self.first_but_position[0],
                    self.first_but_position[1],
                )
            )
            self.first_but_position[1] += 150

    def change_selection(self, move: int) -> None:
        """
        Move the selection to another button.

        Args:
            move: Number of buttons to move by; the selection wraps around.
        """
        self.buttons[self.selection_state].is_selected = False
        self.selection_state = (self.selection_state + move) % len(
            self.buttons
        )
        self.buttons[self.selection_state].is_selected = True


class SelectionDif:
    """
    Difficulty selection screen.

    Attributes:
        selection_state: Index of the selected difficulty.
        backgrounds: Background image of each difficulty.
    """

    def __init__(self) -> None:
        """
        Initialize the selection and load its images.
        """
        self.selection_state: int = 0
        self.backgrounds: list[pg.surface.Surface] = []
        self.load_selection_assets()

    def load_selection_assets(self) -> None:
        """
        Load the background image of each difficulty.
        """
        self.backgrounds.append(
            pg.image.load("textures/difficulty_selection/slect_0.bmp")
        )
        self.backgrounds.append(
            pg.image.load("textures/difficulty_selection/slect_1.bmp")
        )
        self.backgrounds.append(
            pg.image.load("textures/difficulty_selection/slect_2.bmp")
        )
        self.backgrounds.append(
            pg.image.load("textures/difficulty_selection/slect_3.bmp")
        )

    def change_selection(self, move: int) -> None:
        """
        Move the selection to another difficulty.

        Args:
            move: Number of difficulties to move by; the selection wraps
                around.
        """
        self.selection_state = (self.selection_state + move) % len(
            self.backgrounds
        )


class SelectionMap:
    """
    Map selection screen.

    Attributes:
        backgrounds: Background images of the maps, indexed by difficulty.
        selection_state: Index of the selected map.
    """

    def __init__(self) -> None:
        """
        Initialize the selection and load its images.
        """
        self.backgrounds: dict[int, list[pg.surface.Surface]] = {}
        self.selection_state: int = 0
        self.load_assets()

    def load_assets(self) -> None:
        """
        Load the background images of the maps of each difficulty.
        """
        self.backgrounds.update(
            {
                0: [
                    pg.image.load("textures/Map_selection/prairie_select.bmp"),
                    pg.image.load(
                        "textures/Map_selection/prairie_select01.bmp"
                    ),
                    pg.image.load(
                        "textures/Map_selection/prairie_select02.bmp"
                    ),
                ]
            }
        )
        self.backgrounds.update(
            {
                1: [
                    pg.image.load(
                        "textures/Map_selection/medium_map_select.bmp"
                    ),
                    pg.image.load(
                        "textures/Map_selection/medium_map_select_01.bmp"
                    ),
                    pg.image.load(
                        "textures/Map_selection/medium_map_select_02.bmp"
                    ),
                ]
            }
        )
        self.backgrounds.update(
            {
                2: [
                    pg.image.load(
                        "textures/Map_selection/hard_map_select_00.bmp"
                    ),
                    pg.image.load(
                        "textures/Map_selection/hard_map_select_01.bmp"
                    ),
                    pg.image.load(
                        "textures/Map_selection/hard_map_select_02.bmp"
                    ),
                ]
            }
        )
        self.backgrounds.update(
            {
                3: [
                    pg.image.load(
                        "textures/Map_selection/challenger_select.bmp"
                    ),
                ]
            }
        )

    def change_selection(self, move: int, difficulty: SelectionDif) -> None:
        """
        Move the selection to another map of the difficulty.

        The selection wraps around the three maps of a difficulty. The last
        difficulty only has one map.

        Args:
            move: Number of maps to move by.
            difficulty: Difficulty selection, giving the current difficulty.
        """
        if difficulty.selection_state != 3:
            self.selection_state = (self.selection_state + move) % 3
        else:
            self.selection_state = 0
            self.selection_state = (self.selection_state + move) % 1
