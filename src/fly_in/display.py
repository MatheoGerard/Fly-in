import pygame as pg


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

        for hub in hubs:
            pg.draw.circle(
                self.screen,
                (255, 255, 255),
                (
                    (hub.position[0] - min(hub.position[0] for hub in hubs) + 1)
                    * offset_x,
                    (hub.position[1] - min(hub.position[1] for hub in hubs) + 1)
                    * offset_y,
                ),
                50,
            )

    @staticmethod
    def update():
        pg.display.flip()
