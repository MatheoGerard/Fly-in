from .game_state import GameState
from .map_class import Map
from .display import Visualization as visu
from time import sleep


def play_simulation(
    game_manager: GameState, map_instance: Map, vizualizer: visu
) -> None:
    if game_manager.is_play_mode:
        if map_instance:
            map_instance.turn += 1
            for d in map_instance.drones:
                d.move(map_instance.hubs, vizualizer, map_instance)
            sleep(0.5)
