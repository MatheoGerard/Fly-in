import pygame as pg
from .hub import hub as hub_obj
from .main_menu import MainMenu, SelectionDif, SelectionMap
from fly_in import main_menu


class Visualization:
    def __init__(self) -> None:
        self.screen_width: int = 1920
        self.screen_height: int = 1080
        self.screen = self.create_window()

    def create_window(self):
        if self.screen_height < 0 and self.screen_width < 0:
            raise ValueError("screen size must positive!")

        screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Fly-In")

        return screen

    def draw_background(self) -> None:
        self.screen.fill("black")

    def draw_menu_button(self, main_menu_manager: MainMenu) -> None:
        arrow_img = pg.image.load("textures/button_test/arrow.bmp")

        for but in main_menu_manager.buttons:
            if but.is_selected:
                self.screen.blit(
                    arrow_img, (but.position[0] - 300, but.position[1])
                )
            pg.draw.rect(
                self.screen,
                "black",
                (but.position[0], but.position[1], but.dim[0], but.dim[1]),
            )

    def draw_main_menu(
        self, main_menu_manager: MainMenu, launch: bool = False
    ) -> None:
        if launch:
            self.screen.blit(main_menu_manager.background, (0, 0))
            self.draw_menu_button(main_menu_manager)

    def draw_select_dif(
        self, select_dif_manager: SelectionDif, launch: bool
    ) -> None:
        if launch:
            self.screen.blit(
                select_dif_manager.backgrounds[
                    select_dif_manager.selection_state
                ],
                (0, 0),
            )

    def draw_select_map(
        self, select_dif_manager: SelectionDif, map_selector: SelectionMap
    ) -> None:
        self.screen.blit(
            map_selector.backgrounds[select_dif_manager.selection_state][
                map_selector.selection_state
            ],
            (0, 0),
        )

    @staticmethod
    def find_delta_x(hubs) -> int:
        min_x: int = min(hub.position[0] for hub in hubs)
        max_x: int = max(hub.position[0] for hub in hubs)

        return (max_x - min_x) + 2

    @staticmethod
    def find_delta_y(hubs) -> int:
        min_y: int = min(hub.position[1] for hub in hubs)
        max_y: int = max(hub.position[1] for hub in hubs)

        return (max_y - min_y) + 2

    def find_true_positions(self, hubs) -> list[int]:
        return [
            int(self.screen_width / self.find_delta_x(hubs)),
            int(self.screen_height / self.find_delta_y(hubs)),
        ]

    def draw_hub(self, hubs) -> pg.rect.Rect:
        offset_x, offset_y = self.find_true_positions(hubs)
        sub_value_x = min(hub.position[0] for hub in hubs)
        sub_value_y = min(hub.position[1] for hub in hubs)

        for hub in hubs:
            pg.draw.circle(
                self.screen,
                hub.get_color(),
                (
                    hub.get_true_x(sub_value_x, offset_x),
                    hub.get_true_y(sub_value_y, offset_y),
                ),
                25,
            )

    def draw_connexions(self, connection, hubs) -> None:
        offset_x, offset_y = self.find_true_positions(hubs)
        sub_value_x = min(hub.position[0] for hub in hubs)
        sub_value_y = min(hub.position[1] for hub in hubs)

        for co in connection:
            pg.draw.line(
                self.screen,
                pg.Color("white"),
                (
                    co.a.get_true_x(sub_value_x, offset_x),
                    co.a.get_true_y(sub_value_y, offset_y),
                ),
                (
                    co.b.get_true_x(sub_value_x, offset_x),
                    co.b.get_true_y(sub_value_y, offset_y),
                ),
                10,
            )

    @staticmethod
    def update():
        pg.display.flip()
