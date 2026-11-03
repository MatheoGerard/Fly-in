"""
Map model grouping hubs, connections and drones.
"""

from .connexion import Connexion
from .hub import Hub
from .drone import Drone


class Map:
    """
    Map of the simulation.

    Attributes:
        nb_drone: Number of drones of the simulation.
        hubs: All the hubs of the map.
        connexions: All the connections between hubs.
        start: Start hub of the map.
        finish: End hub of the map.
        start_ok: False if the map defines several start hubs.
        end_ok: False if the map defines several end hubs.
        drones: Drones of the simulation.
        turn: Current turn of the simulation.
        turn_timer: Time elapsed since the last turn, in seconds.
    """

    def __init__(
        self, nb_drone: int, hubs: list[Hub], connexions: list[Connexion]
    ) -> None:
        """
        Build the map, create its drones and link the hubs together.

        Args:
            nb_drone: Number of drones to create.
            hubs: Hubs of the map.
            connexions: Connections between the hubs.

        Raises:
            ValueError: If the map has no start or no end hub, or if a
                connection is defined twice.
        """
        self.nb_drone: int = nb_drone
        self.hubs: list[Hub] = hubs
        self.connexions: list[Connexion] = connexions
        self.start: Hub = self.find_start()
        self.finish: Hub = self.find_end()
        self.start_ok: bool = self.validate_start()
        self.end_ok: bool = self.validate_end()
        self.drones: list[Drone] = self.create_drone()
        self.link_hubs()
        self.turn = 0
        self.turn_timer: float = 0.0
        self.start.max_drone = self.nb_drone
        self.finish.max_drone = self.nb_drone
        self.connexions_validate()

    def connexions_validate(self) -> None:
        """
        Check that no connection is defined twice.

        Raises:
            ValueError: If the same connection is defined twice, in either
                direction.
        """
        i = 0
        while i < len(self.connexions):
            other_connexions: list[Connexion] = (
                self.connexions[:i] + self.connexions[i + 1:]
            )
            for c in other_connexions:
                if c.a == self.connexions[i].a and c.b == self.connexions[i].b:
                    raise ValueError("same connexion define twice!")
                if c.a == self.connexions[i].b and c.b == self.connexions[i].a:
                    raise ValueError("same connexion define twice!")
            i += 1

    def link_hubs(self) -> None:
        """
        Register the hubs of each connection as neighbors of each other.
        """
        for co in self.connexions:
            co.a.neighbor.append(co.b)
            co.b.neighbor.append(co.a)

    def create_drone(self) -> list[Drone]:
        """
        Create the drones of the simulation on the start hub.

        Returns:
            The list of created drones.
        """
        r = range(0, self.nb_drone)
        drones: list[Drone] = []

        for i in r:
            drones.append(
                Drone(self.start, i, "textures/perso/pirate_sprite.bmp")
            )

        return drones

    def validate_start(self) -> bool:
        """
        Check that the map has at most one start hub.

        Returns:
            False if several start hubs exist, True otherwise.
        """
        start_nb: int = 0

        for point in self.hubs:
            if point.state == 0:
                start_nb += 1

        if start_nb > 1:
            return False
        return True

    def validate_end(self) -> bool:
        """
        Check that the map has at most one end hub.

        Returns:
            False if several end hubs exist, True otherwise.
        """
        end_nb: int = 0

        for point in self.hubs:
            if point.state == 2:
                end_nb += 1

        if end_nb > 1:
            return False
        return True

    def find_start(self) -> Hub:
        """
        Find the start hub of the map.

        Returns:
            The first hub whose state is 0.

        Raises:
            ValueError: If the map has no start hub.
        """
        for point in self.hubs:
            if point.state == 0:
                return point
        raise ValueError("No start point in map!")

    def find_end(self) -> Hub:
        """
        Find the end hub of the map.

        Returns:
            The first hub whose state is 2.

        Raises:
            ValueError: If the map has no end hub.
        """
        for point in self.hubs:
            if point.state == 2:
                return point
        raise ValueError("No end point in map!")
