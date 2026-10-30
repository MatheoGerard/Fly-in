from .connexion import Connexion
from .hub import Hub
from .drone import Drone


class Map:
    def __init__(
        self, nb_drone: int, hubs: list[Hub], connexions: list[Connexion]
    ) -> None:
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
        self.start.max_drone = self.nb_drone
        self.finish.max_drone = self.nb_drone
        self.connexions_validate()

    def connexions_validate(self) -> None:
        i = 0
        while i < len(self.connexions):
            other_connexions: list[Connexion] = (
                self.connexions[:i] + self.connexions[i + 1 :]
            )
            for c in other_connexions:
                if c.a == self.connexions[i].a and c.b == self.connexions[i].b:
                    raise ValueError("same connexion define twice!")
                if c.a == self.connexions[i].b and c.b == self.connexions[i].a:
                    raise ValueError("same connexion define twice!")
            i += 1

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

    def find_start(self) -> Hub:
        for point in self.hubs:
            if point.state == 0:
                return point
        raise ValueError("No start point in map!")

    def find_end(self) -> Hub:
        for point in self.hubs:
            if point.state == 2:
                return point
        raise ValueError("No end point in map!")
