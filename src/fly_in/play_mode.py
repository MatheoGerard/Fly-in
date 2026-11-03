"""
Automatic play mode of the simulation.
"""

from .game_state import GameState
from .map_class import Map
from .display import Visualization as visu


def play_simulation(
    game_manager: GameState, map_instance: Map | None, vizualizer: visu
) -> None:
    """
    Advance the simulation automatically while play mode is active.

    The elapsed time is accumulated; every 0.5 second the turn counter is
    incremented and each drone moves one step.

    Args:
        game_manager: State of the game, used to know whether play mode is
            active.
        map_instance: Current map, or None if no map is loaded.
        vizualizer: Visualization providing the elapsed time ``dt`` and the
            display.
    """
    if map_instance and game_manager.is_play_mode:
        map_instance.turn_timer += vizualizer.dt
        if map_instance.turn_timer >= 0.5:
            map_instance.turn_timer -= 0.5
            map_instance.turn += 1
            for d in map_instance.drones:
                d.move(map_instance.hubs, vizualizer, map_instance)
