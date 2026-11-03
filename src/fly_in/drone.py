"""
Drone model: movement on the map, animation and path computation.
"""

from __future__ import annotations
import heapq
import math
from collections import defaultdict
from typing import TYPE_CHECKING, Any
import pygame as pg

from .hub import Hub

if TYPE_CHECKING:
    from .display import Visualization
    from fly_in.map_class import Map


class Drone:
    """
    Drone moving from the start hub to the end hub.

    Attributes:
        step: Index of the next entry of ``true_way`` to play.
        current_hub: Hub where the drone currently is.
        last_hub: Hub the drone just left, if any.
        start_position: Screen position of the current hub.
        current_position: Target screen position of the drone.
        render_position: Animated screen position of the drone.
        is_on_end: Whether the drone reached the end hub.
        link: Pair of hubs of the link the drone is on, if any.
        index: Index of the drone.
        texture: Image used to draw the drone.
        true_way: Computed path: one entry per turn, either a hub name or
            ``<hub>-<hub>`` when on a link.
    """

    def __init__(
        self,
        current_hub: Hub,
        index: int,
        text_path: str,
    ) -> None:
        """
        Initialize the drone on a hub.

        Args:
            current_hub: Hub where the drone starts.
            index: Index of the drone.
            text_path: Path of the texture of the drone.
        """
        self.step = 0
        self.current_hub: Hub = current_hub
        self.last_hub: Hub | None = None
        self.start_position: list[int] = []
        self.current_position: list[int] = []
        self.render_position: list[float] = []
        self.is_on_end: bool = False
        self.link: tuple[Hub, Hub] | None = None
        self.index = index
        self.texture = self.load_texture(text_path)
        self.true_way: list[str] = []

    def hub_position(
        self,
        target: Hub,
        hubs: list[Hub],
        visu: Visualization,
    ) -> list[int]:
        """
        Compute the screen position of a hub.

        Args:
            target: Hub whose position is computed.
            hubs: Hubs of the map.
            visu: Visualization used to compute the spacing.

        Returns:
            The position ``[x, y]`` of the hub on screen.
        """
        offset_x, offset_y = visu.find_true_positions(hubs)
        sub_value_x = min(h.position[0] for h in hubs)
        sub_value_y = min(h.position[1] for h in hubs)

        return [
            target.get_true_x(sub_value_x, offset_x),
            target.get_true_y(sub_value_y, offset_y),
        ]

    def define_start_position(
        self, hubs: list[Hub], visu: Visualization
    ) -> None:
        """
        Store the screen position of the current hub.

        Args:
            hubs: Hubs of the map.
            visu: Visualization used to compute the spacing.
        """
        self.start_position = self.hub_position(self.current_hub, hubs, visu)

    def animate(self, target: tuple[int, int], dt: float) -> None:
        """
        Move the rendered position smoothly towards a target.

        The first call places the drone directly on the target.

        Args:
            target: Target position ``(x, y)`` on screen.
            dt: Duration of the last frame in seconds.
        """
        if not self.render_position:
            self.render_position = [
                float(target[0]),
                float(target[1]),
            ]
            return

        factor = 1 - math.exp(-10 * dt)
        for i in range(2):
            pos = self.render_position[i]
            pos += (target[i] - pos) * factor
            if abs(target[i] - pos) < 0.5:
                pos = float(target[i])
            self.render_position[i] = pos

    def load_texture(self, path: str) -> pg.surface.Surface:
        """
        Load the texture of the drone.

        Args:
            path: Path of the image file.

        Returns:
            The loaded surface.
        """
        return pg.image.load(path)

    def enter_link(
        self,
        hubs: list[Hub],
        visu: Visualization,
        a: Hub,
        b: Hub,
    ) -> None:
        """
        Put the drone on the link between two hubs.

        The drone is placed at the middle of the link. The hub it leaves loses
        one drone if the drone was not already on a link.

        Args:
            hubs: Hubs of the map.
            visu: Visualization used to compute the spacing.
            a: Hub at the start of the link.
            b: Hub at the end of the link.
        """
        if self.link is None:
            a.current_nb_drone -= 1
        self.link = (a, b)
        pos_a = self.hub_position(a, hubs, visu)
        pos_b = self.hub_position(b, hubs, visu)
        self.current_position = [
            (pos_a[0] + pos_b[0]) // 2,
            (pos_a[1] + pos_b[1]) // 2,
        ]

    def change_current_hub(
        self,
        hubs: list[Hub],
        visu: Visualization,
        new_hub: Hub,
    ) -> None:
        """
        Move the drone to a new hub and update the drone counters.

        Args:
            hubs: Hubs of the map.
            visu: Visualization used to compute the spacing.
            new_hub: Hub reached by the drone.
        """
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

    def move(
        self,
        hubs: list[Hub],
        visu: Visualization,
        map_instance: Map,
    ) -> None:
        """
        Play the next entry of the computed path.

        An entry ``<hub>-<hub>`` puts the drone on a link, an entry with a hub
        name moves it to that hub. Nothing happens if the path is finished or
        if the drone stays on the same hub.

        Args:
            hubs: Hubs of the map.
            visu: Visualization used to compute the spacing.
            map_instance: Map of the simulation.
        """
        if self.step >= len(self.true_way):
            return
        name_to_hub = {h.name: h for h in map_instance.hubs}
        entry = self.true_way[self.step]
        self.step += 1

        if "-" in entry:
            name_a, name_b = entry.split("-")
            self.enter_link(
                hubs,
                visu,
                name_to_hub[name_a],
                name_to_hub[name_b],
            )
            return

        new_hub = name_to_hub[entry]
        if new_hub is self.current_hub and self.link is None:
            return
        self.change_current_hub(hubs, visu, new_hub)

    def dijsktra(
        self,
        map_instance: Map,
        occupancy: defaultdict[tuple[Any, ...], int],
        max_turn: int = 500,
    ) -> None:
        """
        Compute the path of the drone with a Dijkstra-like search.

        The search runs on states ``(turn, hub)`` and takes into account the
        capacity of hubs and links, the cost of each zone and the priority
        zones. The path found is stored in ``true_way`` and reserved in
        ``occupancy`` so that the next drones avoid it. If no path exists, a
        message is printed and ``true_way`` is left empty.

        Args:
            map_instance: Map of the simulation.
            occupancy: Reservations shared by all the drones, indexed by
                ``(turn, hub)`` or ``(turn, hub, hub)``.
            max_turn: Maximum number of turns explored.
        """
        name_to_hub = {h.name: h for h in map_instance.hubs}
        start = map_instance.start.name
        finish = map_instance.finish.name
        link_cap = {
            tuple(sorted((c.a.name, c.b.name))): c.max_link_capacity
            for c in map_instance.connexions
        }

        def is_free(name: str, turn: int) -> bool:
            """
            Check whether a hub can receive a drone at a given turn.

            Args:
                name: Name of the hub.
                turn: Turn of arrival.

            Returns:
                True if the hub is the start or the end hub, or if it is not
                full at that turn.
            """
            if name in (start, finish):
                return True
            return occupancy[(turn, name)] < name_to_hub[name].max_drone

        def link_free(a: str, b: str, turn: int, new_turn: int) -> bool:
            """
            Check whether a link has room at the next turn.

            Args:
                a: Name of the first hub of the link.
                b: Name of the second hub of the link.
                turn: Turn of departure.
                new_turn: Turn of arrival (not used by the check).

            Returns:
                True if the link is not full at the turn after departure.
            """
            key = tuple(sorted((a, b)))
            return all(
                occupancy[(k, *key)] < link_cap[key]
                for k in range(turn + 1, turn + 2)
            )

        came_from: dict[tuple[int, str], tuple[int, str] | None] = {
            (0, start): None
        }
        score: dict[tuple[int, str], int] = {(0, start): 0}
        queue: list[tuple[int, int, str]] = [(0, 0, start)]
        end: tuple[int, str] | None = None

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
            print("No path available")
            self.true_way = []
            return

        nodes: list[tuple[int, str]] = []
        node: tuple[int, str] | None = end
        while node is not None:
            nodes.append(node)
            node = came_from[node]
        nodes.reverse()

        for (t0, a), (t1, b) in zip(nodes, nodes[1:]):
            if a != b:
                for k in range(t0 + 1, t0 + 2):
                    occupancy[(k, *sorted((a, b)))] += 1

        timeline: list[str] = []
        for (t0, a), (t1, b) in zip(nodes, nodes[1:]):
            on_link = f"{a}-{b}" if a != b else a
            timeline.extend([on_link] * (t1 - t0 - 1))
            timeline.append(b)

        for t1, name in nodes[1:]:
            if name not in (start, finish):
                occupancy[(t1, name)] += 1

        self.true_way = timeline
