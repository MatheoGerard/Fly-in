from .game_state import GameState
from .map_class import Map
from .display import Visualization as visu
from time import sleep


def play_simulation(game_manager: GameState, map_instance: Map) -> None:
    while True:
        if game_manager.is_play_mode:
            for d in map_instance.drones:
                d.move(map_instance.hubs, visu, map_instance)
        sleep(3)
