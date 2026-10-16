from .hub import hub


class Drone:
    def __init__(self, current_hub: hub, index: int) -> None:
        self.current_hub: hub = current_hub
        self.index = index

    def change_current_hub(self, new_hub: hub) -> None:
        self.current_hub = new_hub

    def find_way(self) -> None:
        pass
