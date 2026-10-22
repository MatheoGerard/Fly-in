import heapq
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
        if not self.true_way:
            return
        if self.current_hub is not map_instance.finish:
            self.change_current_hub(hubs, visu, self.true_way[0])
        else:
            print("on the end point")

    def dijsktra(self, map_instance) -> list[str]:
        distance = {hub.name: float("inf") for hub in map_instance.hubs}
        name_to_hub = {hub.name: hub for hub in map_instance.hubs}
        output = {}
        distance[map_instance.start.name] = 0
        priority_queue = [[0, map_instance.start.name]]  # (dist, vertex)

        # -------- 3. Main loop --------
        while priority_queue:
            curr_dist, current_hub = heapq.heappop(priority_queue)

            # Skip stale entries
            if curr_dist != distance[current_hub]:
                continue

            # Explore neighbours
            for point in name_to_hub[current_hub].neighbor:
                dist_trav = curr_dist + point.cost
                if dist_trav < distance[point.name]:
                    distance[point.name] = dist_trav
                    heapq.heappush(priority_queue, [dist_trav, point.name])
                    output[point.name] = current_hub

        return self.path_flip(output, map_instance)

    def path_flip(self, path_rev, map_instance) -> list[str]:
        start_name = map_instance.finish.name
        path = [start_name]

        while map_instance.start.name != path_rev[start_name]:
            start_name = path_rev.get(start_name)
            path.append(start_name)

        print(path[::-1])
        return path[::-1]
