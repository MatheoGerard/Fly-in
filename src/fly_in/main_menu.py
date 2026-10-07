import pygame as pg
from .game_state import GameState


class Button:
    def __init__(
        self, selected: bool, text_in_button: str, x: int, y: int
    ) -> None:
        self.is_selected: bool = selected
        self.text: str = text_in_button
        self.position: list[int] = [x, y]
        self.dim: list[int] = [600, 150]


class MainMenu:
    def __init__(
        self, background_path: str, game_manager: GameState, options: int
    ) -> None:
        self.nb_options: int = options
        self.selection_state: int = 0
        self.background = pg.image.load(background_path)
        self.buttons: list[Button] = []
        self.first_but_position: list[int] = [1000, 600]

    def create_button(self) -> None:
        self.buttons.append(
            Button(
                True,
                "PLAY",
                self.first_but_position[0],
                self.first_but_position[1],
            ),
        )

        self.first_but_position[1] += 200

        for _ in range(0, self.nb_options - 1):
            self.buttons.append(
                Button(
                    False,
                    "QUIT",
                    self.first_but_position[0],
                    self.first_but_position[1],
                )
            )
            self.first_but_position[1] += 100

    def change_selection(self, move: int) -> None:
        self.buttons[self.selection_state].is_selected = False
        self.selection_state = (self.selection_state + move) % len(
            self.buttons
        )
        self.buttons[self.selection_state].is_selected = True


class SelectionDif:
    def __init__(self) -> None:
        self.selection_state: int = 0
        self.backgrounds = []
        self.load_selection_assets()

    def load_selection_assets(self) -> None:
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
        print(len(self.backgrounds))

    def change_selection(self, move: int) -> None:
        self.selection_state = (self.selection_state + move) % len(
            self.backgrounds
        )


class SelectionMap:
    def __init__(self) -> None:
        self.backgrounds: dict[int, list[pg.Surface]] = {}
        self.selection_state: int = 0
        self.load_assets()

    def load_assets(self) -> None:
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
            {1: [pg.image.load("textures/Map_selection/medium_map.bmp")]}
        )
        self.backgrounds.update(
            {2: [pg.image.load("textures/Map_selection/hard_map.bmp")]}
        )

    def change_selection(self, move: int) -> None:
        self.selection_state = (self.selection_state + move) % 3
