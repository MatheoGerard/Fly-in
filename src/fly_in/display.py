import pygame as pg
from .hub import hub as hub_obj


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

        screen.fill((30, 30, 30))
        pg.display.flip()

        return screen

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
            )

    @staticmethod
    def update():
        pg.display.flip()
