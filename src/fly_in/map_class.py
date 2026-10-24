from .connexion import Connexion
from .hub import hub
from .drone import Drone


class Map:
    def __init__(
        self, nb_drone: int, hubs: list[hub], connexions: list[Connexion]
    ) -> None:
        self.nb_drone: int = nb_drone
        self.hubs: list[hub] = hubs
        self.connexions: list[Connexion] = connexions
        self.start: hub = self.find_start()
        self.finish: hub = self.find_end()
        self.start_ok: bool = self.validate_start()
        self.end_ok: bool = self.validate_end()
        self.drones: list[Drone] = self.create_drone()
        self.link_hubs()
        self.turn = 0

    def link_hubs(self) -> None:
        for co in self.connexions:
            co.a.neighbor.append(co.b)
            co.b.neighbor.append(co.a)

    def create_drone(self) -> list[Drone]:
        r = range(0, self.nb_drone)
        drones: list[Drone] = []

        for i in r:
            drones.append(
                Drone(self.start, i, "textures/perso/pirate_sprite.bmp")
            )

        return drones

    def validate_start(self) -> bool:
        start_nb: int = 0

        for point in self.hubs:
            if point.state == 0:
                start_nb += 1

        if start_nb > 1:
            return False
        return True

    def validate_end(self) -> bool:
        end_nb: int = 0

        for point in self.hubs:
            if point.state == 2:
                end_nb += 1

        if end_nb > 1:
            return False
        return True

    def find_start(self) -> hub:
        for point in self.hubs:
            if point.state == 0:
                return point
        raise ValueError("No start point in map!")

    def find_end(self) -> hub:
        for point in self.hubs:
            if point.state == 2:
                return point
        raise ValueError("No end point in map!")
