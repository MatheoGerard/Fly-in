from .hub import hub


class Map:
    def __init__(self) -> None:
        self.nb_drone: int
        self.hubs: list[hub]
        self.start: hub
        self.finish: hub
