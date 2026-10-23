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
        """
        Crée un drone placé sur un hub de départ.
        """
        self.step = 0
        self.current_hub: hub = current_hub
        self.last_hub: hub | None = None
        self.start_position: list[int] = []
        self.current_position: list[int] = []
        self.is_on_end: bool = False
        self.index = index
        self.texture = self.load_texture(text_path)
        self.true_way: list[str] = []

    def define_start_position(self, hubs: list[hub], visu) -> None:
        """
        Calcule la position à l'écran du hub courant.
        """
        offset_x, offset_y = visu.find_true_positions(hubs)
        sub_value_x = min(h.position[0] for h in hubs)
        sub_value_y = min(h.position[1] for h in hubs)

        self.start_position = [
            self.current_hub.get_true_x(sub_value_x, offset_x),
            self.current_hub.get_true_y(sub_value_y, offset_y),
        ]

    def load_texture(self, path: str) -> pg.surface.Surface:
        """
        Charge l'image du drone.
        """
        return pg.image.load(path)

    def change_current_hub(self, hubs: list[hub], visu, new_hub: hub) -> None:
        """
        Déplace le drone vers new_hub et met à jour les compteurs.
        """
        self.last_hub = self.current_hub
        self.current_hub = new_hub

        self.define_start_position(hubs, visu)
        self.current_position = self.start_position.copy()

        self.last_hub.current_nb_drone -= 1
        self.current_hub.current_nb_drone += 1

        if new_hub.state == 2:
            self.is_on_end = True

    def move(self, hubs: list[hub], visu, map_instance) -> None:
        """
        Avance d'un tour le long de true_way (ou attend).
        """
        if self.step >= len(self.true_way):
            return
        name_to_hub = {h.name: h for h in map_instance.hubs}
        new_hub = name_to_hub[self.true_way[self.step]]
        self.step += 1
        if new_hub is self.current_hub:
            return
        self.change_current_hub(hubs, visu, new_hub)

    def dijsktra(
        self,
        map_instance,
        occupancy: dict,
        max_turn: int = 500,
    ) -> None:
        """
        Planifie le chemin dans le temps en tenant compte des
        réservations (occupancy) et en favorisant les hubs priority.
        """
        name_to_hub = {h.name: h for h in map_instance.hubs}
        start = map_instance.start.name
        finish = map_instance.finish.name

        def is_free(name: str, turn: int) -> bool:
            if name in (start, finish):  # capacité illimitée
                return True
            return occupancy[(turn, name)] < name_to_hub[name].max_drone

        came_from = {(0, start): None}
        score = {(0, start): 0}  # nb de hubs priority traversés
        queue = [(0, 0, start)]  # (tour, -score, hub)
        end = None

        while queue:
            turn, neg_score, name = heapq.heappop(queue)
            if -neg_score != score[(turn, name)]:
                continue  # entrée périmée, un meilleur score existe
            if name == finish:
                end = (turn, name)
                break
            if turn >= max_turn:
                continue

            options = [(1, name)]  # attendre
            options += [
                (max(1, int(n.cost)), n.name)
                for n in name_to_hub[name].neighbor
                if n.cost != float("inf")
            ]

            for duration, nxt in options:
                new_turn = turn + duration
                if not is_free(nxt, new_turn):
                    continue
                # pendant un trajet long, on reste "sur" le hub d'origine
                if any(
                    not is_free(name, t) for t in range(turn + 1, new_turn)
                ):
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

        # reconstruction des noeuds (tour, hub)
        nodes = []
        node = end
        while node is not None:
            nodes.append(node)
            node = came_from[node]
        nodes.reverse()

        # timeline[i] = hub où se trouve le drone après le tour i+1
        timeline = []
        for (t0, a), (t1, b) in zip(nodes, nodes[1:]):
            timeline.extend([a] * (t1 - t0 - 1))
            timeline.append(b)

        # réservation des hubs pour les drones suivants
        for i, name in enumerate(timeline):
            if name not in (start, finish):
                occupancy[(i + 1, name)] += 1

        self.true_way = timeline
