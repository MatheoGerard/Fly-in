import pygame as pg

from .connexion import Connexion
from .drone import Drone
from .hub import Hub
from .main_menu import MainMenu, SelectionDif, SelectionMap
from .map_class import Map


class Visualization:
    def __init__(self) -> None:
        self.screen_width: int = 1920
        self.screen_height: int = 1080
        self.screen = self.create_window()

    def create_window(self) -> pg.surface.Surface:
        if self.screen_height < 0 and self.screen_width < 0:
            raise ValueError("screen size must positive!")

        screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Fly-In")

        return screen

    def draw_background(self, current_dif: int, current_map: int) -> None:
        map_texture: pg.surface.Surface

        if current_dif == 0:
            if current_map == 0:
                map_texture = pg.image.load(
                    "textures/maps_textures/map_meadow.bmp"
                )
                self.screen.blit(map_texture, (0, 0))
            elif current_map == 1:
                map_texture = pg.image.load(
                    "textures/maps_textures/map_forest.bmp"
                )
                self.screen.blit(map_texture, (0, 0))
            else:
                map_texture = pg.image.load(
                    "textures/maps_textures/map_castle.bmp"
                )
                self.screen.blit(map_texture, (0, 0))
        elif current_dif == 1:
            if current_map == 0:
                map_texture = pg.image.load(
                    "textures/maps_textures/map_lava.bmp"
                )
                self.screen.blit(map_texture, (0, 0))
            elif current_map == 1:
                map_texture = pg.image.load(
                    "textures/maps_textures/map_volcano.bmp"
                )
                self.screen.blit(map_texture, (0, 0))
            else:
                map_texture = pg.image.load(
                    "textures/maps_textures/map_prison.bmp"
                )
                self.screen.blit(map_texture, (0, 0))
        elif current_dif == 2:
            if current_map == 0:
                map_texture = pg.image.load(
                    "textures/maps_textures/map_graveyard.bmp"
                )
                self.screen.blit(map_texture, (0, 0))
            elif current_map == 1:
                map_texture = pg.image.load(
                    "textures/maps_textures/map_mansion.bmp"
                )
                self.screen.blit(map_texture, (0, 0))
            elif current_map == 2:
                map_texture = pg.image.load(
                    "textures/maps_textures/map_skull.bmp"
                )
                self.screen.blit(map_texture, (0, 0))
        elif current_dif == 3:
            map_texture = pg.image.load("textures/maps_textures/map_moon.bmp")
            self.screen.blit(map_texture, (0, 0))
        else:
            self.screen.fill("black")

    def draw_menu_button(self, main_menu_manager: MainMenu) -> None:
        arrow_img = pg.image.load("textures/button_test/arrow.bmp")

        for but in main_menu_manager.buttons:
            if but.is_selected:
                self.screen.blit(
                    arrow_img, (but.position[0], but.position[1] + 10)
                )
            # pg.draw.rect(
            #     self.screen,
            #     "black",
            #     (but.position[0], but.position[1], but.dim[0], but.dim[1]),
            # )
            # but_txt = pg.font.SysFont("Comic Sans MS", 75)
            # txt = but_txt.render(but.text, False, "white")
            #
            # self.screen.blit(
            #     txt,
            #     [
            #         but.position[0]
            #         + int(but.dim[0] / 2)
            #         - int(txt.get_width() / 2),
            #         but.position[1] + int(but.dim[1] / 2),
            #     ],
            # )

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
    def find_delta_x(hubs: list[Hub]) -> int:
        min_x: int = min(hub.position[0] for hub in hubs)
        max_x: int = max(hub.position[0] for hub in hubs)

        return (max_x - min_x) + 2

    @staticmethod
    def find_delta_y(hubs: list[Hub]) -> int:
        min_y: int = min(hub.position[1] for hub in hubs)
        max_y: int = max(hub.position[1] for hub in hubs)

        return (max_y - min_y) + 2

    def find_true_positions(self, hubs: list[Hub]) -> list[int]:
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

    def draw_hub(self, hubs: list[Hub]) -> None:
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
        if turn > total:
            turn = total
        turn_txt = pg.font.SysFont("Comic Sans MS", 50)
        turn_surface = turn_txt.render(f"{turn}/{total}", False, "white")

        self.screen.blit(turn_surface, (0, 0))

    def draw_hub_name(self, point: Hub, pos: list[int]) -> None:
        hub_txt = pg.font.SysFont("Comic Sans MS", 50)
        txt_surface = hub_txt.render(
            f"{point.name} {point.current_nb_drone}/{point.max_drone}",
            False,
            "white",
        )

        self.screen.blit(
            txt_surface,
            [pos[0] - int(txt_surface.get_width() / 2), pos[1] + 30],
        )

    def draw_connexions(
        self, connection: list[Connexion], hubs: list[Hub]
    ) -> None:
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
                2,
            )

    def draw_loop(
        self, map_instance: Map | None, current_dif: int, current_map: int
    ) -> None:
        if map_instance:
            self.draw_background(current_dif, current_map)
            self.draw_connexions(map_instance.connexions, map_instance.hubs)
            self.draw_hub(map_instance.hubs)
            self.draw_drones(map_instance.drones)
            self.draw_turn(
                map_instance.turn,
                max((len(d.true_way) for d in map_instance.drones), default=0),
            )

    @staticmethod
    def update() -> None:
        pg.display.flip()
