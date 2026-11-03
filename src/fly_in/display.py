"""
Rendering of the menus and of the simulation.
"""

import pygame as pg

from .connexion import Connexion
from .drone import Drone
from .hub import Hub
from .main_menu import MainMenu, SelectionDif, SelectionMap
from .map_class import Map


class Visualization:
    """
    Draw the menus and the simulation on the pygame window.

    Attributes:
        screen_width: Width of the window in pixels.
        screen_height: Height of the window in pixels.
        clock: Clock used to limit the frame rate.
        dt: Duration of the last frame in seconds.
        screen: Surface of the window.
    """

    def __init__(self) -> None:
        """
        Initialize the window size, the clock and create the window.
        """
        self.screen_width: int = 1920
        self.screen_height: int = 1080
        self.clock: pg.time.Clock = pg.time.Clock()
        self.dt: float = 0.0
        self.screen = self.create_window()

    def create_window(self) -> pg.surface.Surface:
        """
        Create the pygame window.

        Returns:
            The surface of the created window.

        Raises:
            ValueError: If both the screen width and the screen height are
                negative.
        """
        if self.screen_height < 0 and self.screen_width < 0:
            raise ValueError("screen size must positive!")

        screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Fly-In")

        return screen

    def draw_background(self, current_dif: int, current_map: int) -> None:
        """
        Draw the background matching the difficulty and the map.

        The screen is filled with black if no texture matches.

        Args:
            current_dif: Index of the current difficulty.
            current_map: Index of the current map in the difficulty.
        """
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
        """
        Draw an arrow next to the selected menu button.

        Args:
            main_menu_manager: Main menu holding the buttons.
        """
        arrow_img = pg.image.load("textures/button_test/arrow.bmp")

        for but in main_menu_manager.buttons:
            if but.is_selected:
                self.screen.blit(
                    arrow_img, (but.position[0], but.position[1] + 10)
                )

    def draw_main_menu(
        self, main_menu_manager: MainMenu, launch: bool = False
    ) -> None:
        """
        Draw the main menu.

        Args:
            main_menu_manager: Main menu to draw.
            launch: If True, the menu is drawn.
        """
        if launch:
            self.screen.blit(main_menu_manager.background, (0, 0))
            self.draw_menu_button(main_menu_manager)

    def draw_select_dif(
        self, select_dif_manager: SelectionDif, launch: bool
    ) -> None:
        """
        Draw the difficulty selection screen.

        Args:
            select_dif_manager: Difficulty selection to draw.
            launch: If True, the screen is drawn.
        """
        if launch:
            self.screen.blit(
                select_dif_manager.backgrounds[
                    select_dif_manager.selection_state
                ],
                (0, 0),
            )

    def draw_select_map(
        self,
        select_dif_manager: SelectionDif,
        map_selector: SelectionMap,
    ) -> None:
        """
        Draw the map selection screen.

        Args:
            select_dif_manager: Difficulty selection, giving the current
                difficulty.
            map_selector: Map selection, giving the current map.
        """
        self.screen.blit(
            map_selector.backgrounds[select_dif_manager.selection_state][
                map_selector.selection_state
            ],
            (0, 0),
        )

    @staticmethod
    def find_delta_x(hubs: list[Hub]) -> int:
        """
        Compute the horizontal size of the map in coordinates.

        Args:
            hubs: Hubs of the map.

        Returns:
            The distance between the smallest and the largest x coordinate,
            plus a margin of 2.
        """
        min_x: int = min(hub.position[0] for hub in hubs)
        max_x: int = max(hub.position[0] for hub in hubs)

        return (max_x - min_x) + 2

    @staticmethod
    def find_delta_y(hubs: list[Hub]) -> int:
        """
        Compute the vertical size of the map in coordinates.

        Args:
            hubs: Hubs of the map.

        Returns:
            The distance between the smallest and the largest y coordinate,
            plus a margin of 2.
        """
        min_y: int = min(hub.position[1] for hub in hubs)
        max_y: int = max(hub.position[1] for hub in hubs)

        return (max_y - min_y) + 2

    def find_true_positions(self, hubs: list[Hub]) -> list[int]:
        """
        Compute the pixel spacing between two coordinates of the map.

        Args:
            hubs: Hubs of the map.

        Returns:
            A list ``[offset_x, offset_y]`` giving the horizontal and vertical
            spacing in pixels.
        """
        return [
            int(self.screen_width / self.find_delta_x(hubs)),
            int(self.screen_height / self.find_delta_y(hubs)),
        ]

    def draw_drones(self, drones: list[Drone]) -> None:
        """
        Draw the drones with a smooth animation.

        Drones sharing the same position are spread on a grid of five columns
        so that they do not overlap.

        Args:
            drones: Drones to draw.
        """
        seen: dict[tuple[int, int], int] = {}
        for d in drones:
            key = (
                d.current_position[0],
                d.current_position[1],
            )
            rank = seen.get(key, 0)
            seen[key] = rank + 1
            dx = (rank % 5) * 14 - 28
            dy = (rank // 5) * 14 - 28
            d.animate((key[0] + dx, key[1] + dy), self.dt)
            self.screen.blit(
                d.texture,
                (
                    int(d.render_position[0] - d.texture.get_width() / 2),
                    int(d.render_position[1] - d.texture.get_height() / 2),
                ),
            )

    def draw_hub(self, hubs: list[Hub]) -> None:
        """
        Draw every hub as a colored circle.

        Args:
            hubs: Hubs to draw.
        """
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
        """
        Draw the turn counter, formatted as ``turn/total``, in the top left
        corner.

        Args:
            turn: Current turn, capped to ``total`` when displayed.
            total: Total number of turns of the simulation.
        """
        if turn > total:
            turn = total
        turn_txt = pg.font.SysFont("Comic Sans MS", 50)
        turn_surface = turn_txt.render(f"{turn}/{total}", False, "white")

        self.screen.blit(turn_surface, (0, 0))

    def draw_hub_name(self, point: Hub, pos: list[int]) -> None:
        """
        Draw the name and the occupancy of a hub below it, formatted as ``name
        current/max``.

        Args:
            point: Hub whose name is drawn.
            pos: Position ``[x, y]`` of the hub on screen.
        """
        hub_txt = pg.font.SysFont("Comic Sans MS", 50)
        txt_surface = hub_txt.render(
            f"{point.name} " f"{point.current_nb_drone}/{point.max_drone}",
            False,
            "white",
        )

        self.screen.blit(
            txt_surface,
            [
                pos[0] - int(txt_surface.get_width() / 2),
                pos[1] + 30,
            ],
        )

    def draw_connexions(
        self,
        connection: list[Connexion],
        hubs: list[Hub],
    ) -> None:
        """
        Draw every connection as a line between its two hubs.

        Args:
            connection: Connections to draw.
            hubs: Hubs of the map.
        """
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
        self,
        map_instance: Map | None,
        current_dif: int,
        current_map: int,
    ) -> None:
        """
        Draw a whole frame of the simulation: background, connections, hubs,
        drones and turn counter.

        Args:
            map_instance: Map to draw, nothing is drawn if None.
            current_dif: Index of the current difficulty.
            current_map: Index of the current map in the difficulty.
        """
        if map_instance:
            self.draw_background(current_dif, current_map)
            self.draw_connexions(
                map_instance.connexions,
                map_instance.hubs,
            )
            self.draw_hub(map_instance.hubs)
            self.draw_drones(map_instance.drones)
            self.draw_turn(
                map_instance.turn,
                max(
                    (len(d.true_way) for d in map_instance.drones),
                    default=0,
                ),
            )

    def update(self) -> None:
        """
        Refresh the display and limit the frame rate to 60 FPS.

        The duration of the frame is stored in ``dt`` and capped to 0.1 second.
        """
        pg.display.flip()
        self.dt = min(self.clock.tick(60) / 1000, 0.1)
