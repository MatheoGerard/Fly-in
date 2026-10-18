import pygame as pg
from .hub import hub


class Drone:
    def __init__(
        self,
        current_hub: hub,
        index: int,
        text_path: str,
    ) -> None:
        self.current_hub: hub = current_hub
        self.start_position: list[int] = []
        self.current_position: list[int] = self.start_position
        self.index = index
        self.texture = self.laod_texture(text_path)

    def define_start_position(self, hubs: list[hub], visu) -> None:
        offset_x, offset_y = visu.find_true_positions(hubs)
        sub_value_x = min(hub.position[0] for hub in hubs)
        sub_value_y = min(hub.position[1] for hub in hubs)

        self.start_position = [
            self.current_hub.get_true_x(sub_value_x, offset_x),
            self.current_hub.get_true_y(sub_value_y, offset_y),
        ]

    def laod_texture(self, path: str) -> pg.surface.Surface:
        return pg.image.load(path)

    def change_current_hub(self, new_hub: hub) -> None:
        self.current_hub = new_hub

    def find_way(self) -> None:
        pass
