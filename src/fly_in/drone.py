import pygame as pg
from .hub import hub


class Drone:
    def __init__(
        self,
        current_hub: hub,
        index: int,
        text_path: str,
    ) -> None:
        self.step = 0
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

    def change_current_hub(self, hubs: list[hub], visu, new_hub: hub) -> None:
        offset_x, offset_y = visu.find_true_positions(hubs)
        sub_value_x = min(hub.position[0] for hub in hubs)
        sub_value_y = min(hub.position[1] for hub in hubs)

        self.last_hub = self.current_hub
        self.current_hub = new_hub
        print(f"last hub is {self.last_hub.name}")
        print(f"new hub is {new_hub.name}")
        print(f"current is {self.current_hub.name}")
        self.start_position = [
            new_hub.get_true_x(sub_value_x, offset_x),
            new_hub.get_true_y(sub_value_y, offset_y),
        ]
        self.current_position = self.start_position
        self.define_start_position(hubs, visu)

        self.last_hub.current_nb_drone -= 1
        self.current_hub.current_nb_drone += 1

        if new_hub.state == 2:
            self.is_on_end = True

    def move(self, hubs: list[hub], visu, map_instance) -> None:
        if self.current_hub is not map_instance.finish:
            self.change_current_hub(hubs, visu, self.true_way[0])
        else:
            print("on the end point")

    def find_way(self, current: hub) -> None:
        print(f"on part de {current.name}")
        ways: list[list[hub]] = []
        start_list: list[hub] = [current]
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
                    return

                for p in possibilities:
                    new_list: list[hub] = way.copy()
                    new_list.append(p)
                    ways.append(new_list)

        self.true_way = true_way[1:]
        print([name.name for name in self.true_way])
