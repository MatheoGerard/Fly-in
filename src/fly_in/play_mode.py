from .game_state import GameState
from .map_class import Map
from .display import Visualization as visu


def play_simulation(
    game_manager: GameState, map_instance: Map | None, vizualizer: visu
) -> None:
    if map_instance and game_manager.is_play_mode:
        map_instance.turn_timer += vizualizer.dt
        if map_instance.turn_timer >= 0.5:
            map_instance.turn_timer -= 0.5
            map_instance.turn += 1
            for d in map_instance.drones:
                d.move(map_instance.hubs, vizualizer, map_instance)
