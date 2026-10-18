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
        self.last_hub: hub | None = None
        self.start_position: list[int] = []
        self.current_position: list[int] = []
        self.is_on_end: bool = False
        self.index = index
        self.texture = self.laod_texture(text_path)
        self.true_way = []

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
        self.last_hub = self.current_hub
        self.current_hub = new_hub

        self.last_hub.current_nb_drone -= 1
        self.current_hub.current_nb_drone += 1

        if new_hub.state == 2:
            self.is_on_end = True

    def move(self) -> None:
        self.change_current_hub(self.true_way[0])

    def find_way(self) -> None:
        ways: list[list[hub]] = []
        start_list: list[hub] = [self.current_hub]
        find: bool = False
        ways.append(start_list)
        true_way: list[hub] = []

        while not find:
            possibilities: list[hub] = []

            for way in ways:
                if way[-1].state == 2:
                    find = True
                    true_way = way
                    break

                for h in way[-1].neighbor:
                    if h.zone_type == "blocked":
                        continue
                    elif h.is_full():
                        continue
                    elif h == self.last_hub:
                        continue
                    elif h.state == 2:
                        possibilities.clear()
                        possibilities.append(h)
                        break
                    possibilities.append(h)

                if not possibilities:
                    print("no ways")
                    break

                for p in possibilities:
                    new_list: list[hub] = way.copy()
                    new_list.append(p)
                    ways.append(new_list)

        self.true_way = true_way
        for h in self.true_way:
            print(h.name)
