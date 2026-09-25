from .hub import hub


class Connexion:
    def __init__(self, a: hub, b: hub) -> None:
        self.a: hub = a
        self.b: hub = b
