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
        self.link: tuple[hub, hub] | None = None
        self.index = index
        self.texture = self.load_texture(text_path)
        self.true_way: list[str] = []

    def hub_position(self, target: hub, hubs: list[hub], visu) -> list[int]:
        offset_x, offset_y = visu.find_true_positions(hubs)
        sub_value_x = min(h.position[0] for h in hubs)
        sub_value_y = min(h.position[1] for h in hubs)

        return [
            target.get_true_x(sub_value_x, offset_x),
            target.get_true_y(sub_value_y, offset_y),
        ]

    def define_start_position(self, hubs: list[hub], visu) -> None:
        self.start_position = self.hub_position(self.current_hub, hubs, visu)

    def load_texture(self, path: str) -> pg.surface.Surface:
        return pg.image.load(path)

    def enter_link(self, hubs: list[hub], visu, a: hub, b: hub) -> None:
        if self.link is None:
            a.current_nb_drone -= 1
        self.link = (a, b)
        pos_a = self.hub_position(a, hubs, visu)
        pos_b = self.hub_position(b, hubs, visu)
        self.current_position = [
            (pos_a[0] + pos_b[0]) // 2,
            (pos_a[1] + pos_b[1]) // 2,
        ]

    def change_current_hub(self, hubs: list[hub], visu, new_hub: hub) -> None:
        self.last_hub = self.current_hub
        self.current_hub = new_hub

        self.define_start_position(hubs, visu)
        self.current_position = self.start_position.copy()

        if self.link is None:
            self.last_hub.current_nb_drone -= 1
        self.link = None
        self.current_hub.current_nb_drone += 1

        if new_hub.state == 2:
            self.is_on_end = True

    def move(self, hubs: list[hub], visu, map_instance) -> None:
        if self.step >= len(self.true_way):
            return
        name_to_hub = {h.name: h for h in map_instance.hubs}
        entry = self.true_way[self.step]
        self.step += 1

        if "-" in entry:
            name_a, name_b = entry.split("-")
            self.enter_link(
                hubs, visu, name_to_hub[name_a], name_to_hub[name_b]
            )
            return

        new_hub = name_to_hub[entry]
        if new_hub is self.current_hub and self.link is None:
            return
        self.change_current_hub(hubs, visu, new_hub)

    def dijsktra(
        self,
        map_instance,
        occupancy: dict,
        max_turn: int = 500,
    ) -> None:
        name_to_hub = {h.name: h for h in map_instance.hubs}
        start = map_instance.start.name
        finish = map_instance.finish.name
        link_cap = {
            tuple(sorted((c.a.name, c.b.name))): c.max_link_capacity
            for c in map_instance.connexions
        }

        def is_free(name: str, turn: int) -> bool:
            if name in (start, finish):
                return True
            return occupancy[(turn, name)] < name_to_hub[name].max_drone

        def link_free(a: str, b: str, turn: int, new_turn: int) -> bool:
            key = tuple(sorted((a, b)))
            return all(
                occupancy[(k, *key)] < link_cap[key]
                for k in range(turn + 1, turn + 2)
            )

        came_from = {(0, start): None}
        score = {(0, start): 0}
        queue = [(0, 0, start)]
        end = None

        while queue:
            turn, neg_score, name = heapq.heappop(queue)
            if -neg_score != score[(turn, name)]:
                continue
            if name == finish:
                end = (turn, name)
                break
            if turn >= max_turn:
                continue

            options = [(1, name)]
            options += [
                (max(1, int(n.cost)), n.name)
                for n in name_to_hub[name].neighbor
                if n.cost != float("inf")
            ]

            for duration, nxt in options:
                new_turn = turn + duration
                if not is_free(nxt, new_turn):
                    continue
                if nxt != name and not link_free(name, nxt, turn, new_turn):
                    continue

                new_score = -neg_score
                if nxt != name and name_to_hub[nxt].zone_type == "priority":
                    new_score += 1

                state = (new_turn, nxt)
                if state in came_from and score[state] >= new_score:
                    continue
                came_from[state] = (turn, name)
                score[state] = new_score
                heapq.heappush(queue, (new_turn, -new_score, nxt))

        if end is None:
            print("Aucun chemin disponible")
            self.true_way = []
            return

        nodes = []
        node = end
        while node is not None:
            nodes.append(node)
            node = came_from[node]
        nodes.reverse()

        for (t0, a), (t1, b) in zip(nodes, nodes[1:]):
            if a != b:
                for k in range(t0 + 1, t0 + 2):
                    occupancy[(k, *sorted((a, b)))] += 1

        timeline = []
        for (t0, a), (t1, b) in zip(nodes, nodes[1:]):
            on_link = f"{a}-{b}" if a != b else a
            timeline.extend([on_link] * (t1 - t0 - 1))
            timeline.append(b)

        for t1, name in nodes[1:]:
            if name not in (start, finish):
                occupancy[(t1, name)] += 1

        self.true_way = timeline
