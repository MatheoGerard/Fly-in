import pygame as pg
from .drone import Drone
from .hub import hub as hub_obj
from .main_menu import MainMenu, SelectionDif, SelectionMap


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
            but_txt = pg.font.SysFont("Comic Sans MS", 75)
            txt = but_txt.render(but.text, False, "white")

            self.screen.blit(
                txt,
                [
                    but.position[0]
                    + int(but.dim[0] / 2)
                    - int(txt.get_width() / 2),
                    but.position[1] + int(but.dim[1] / 2),
                ],
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

    def draw_drones(self, drones: list[Drone]) -> None:
        seen: dict[tuple[int, int], int] = {}
        for d in drones:
            key = (d.current_position[0], d.current_position[1])
            rank = seen.get(key, 0)
            seen[key] = rank + 1
            dx = (rank % 5) * 14 - 28
            dy = (rank // 5) * 14 - 28
            self.screen.blit(
                d.texture,
                (
                    d.current_position[0]
                    - int(d.texture.get_width() / 2)
                    + dx,
                    d.current_position[1]
                    - int(d.texture.get_height() / 2)
                    + dy,
                ),
            )

    def draw_hub(self, hubs) -> None:
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

    def draw_turn(self, turn: int, total: int) -> None:
        turn_txt = pg.font.SysFont("Comic Sans MS", 50)
        turn_surface = turn_txt.render(f"{turn}/{total}", False, "white")

        self.screen.blit(turn_surface, (0, 0))

    def draw_hub_name(self, point: hub_obj, pos: list[int]) -> None:
        hub_txt = pg.font.SysFont("Comic Sans MS", 75)
        txt_surface = hub_txt.render(point.name, False, "white")

        self.screen.blit(
            txt_surface,
            [pos[0] - int(txt_surface.get_width() / 2), pos[1] + 30],
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
                5,
            )

    @staticmethod
    def update():
        pg.display.flip()
