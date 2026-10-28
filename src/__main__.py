import pygame as pg
from typing import Any
from fly_in import Visualization as vizu
from fly_in import (
    Map,
    read_input,
    GameState,
    MainMenu,
    SelectionDif,
    SelectionMap,
    mouse_hover,
    play_simulation,
    simu_init,
    Drone,
    Connexion,
)
from collections import defaultdict
from pydantic import ValidationError

from fly_in.hub import Hub


def load_maps() -> list[list[str]]:
    easy: list[str] = []
    medium: list[str] = []
    hard: list[str] = []
    chalenger: list[str] = []

    easy.append("maps/easy/01_linear_path.txt")
    easy.append("maps/easy/02_simple_fork.txt")
    easy.append("maps/easy/03_basic_capacity.txt")

    medium.append("maps/medium/01_dead_end_trap.txt")
    medium.append("maps/medium/02_circular_loop.txt")
    medium.append("maps/medium/03_priority_puzzle.txt")

    hard.append("maps/hard/01_maze_nightmare.txt")
    hard.append("maps/hard/02_capacity_hell.txt")
    hard.append("maps/hard/03_ultimate_challenge.txt")

    chalenger.append("maps/challenger/01_the_impossible_dream.txt")

    return [easy, medium, hard, chalenger]


def print_simulation(drones: list[Drone], start_name: str) -> None:
    nb_turns = max((len(d.true_way) for d in drones), default=0)

    for turn in range(nb_turns):
        moves = []
        for d in drones:
            if turn >= len(d.true_way):
                continue
            previous = d.true_way[turn - 1] if turn > 0 else start_name
            current = d.true_way[turn]
            if current != previous:
                moves.append(f"D{d.index}-{current}")
        print(" ".join(moves), flush=True, file=open("text.txt", "a"))

    print(f"Total : {nb_turns} tours", flush=True, file=open("text.txt", "a"))


if __name__ == "__main__":
    try:
        maps_path: list[list[str]] = load_maps()

        pg.init()
        pg.font.init()

        is_parsed: bool = False

        game_manager = GameState()
        main_menu_manager: MainMenu = MainMenu(
            "textures/backrgound/PO_main_background.bmp", game_manager, 2
        )
        main_menu_manager.create_button()
        difficulty_select = SelectionDif()
        map_select = SelectionMap()
        vizualizer = vizu()
        vizualizer.create_window()
        map_instance: Map | None = None

        content: str = ""
        connexions: list[Connexion] = []
        hubs: list[Hub] = []

        while game_manager.game_running:
            if game_manager.is_main_menu:
                vizualizer.draw_main_menu(main_menu_manager, True)
                is_parsed = False
            elif game_manager.is_difficulty_select:
                vizualizer.draw_select_dif(difficulty_select, True)
                is_parsed = False
            elif game_manager.is_map_selection:
                vizualizer.draw_select_map(difficulty_select, map_select)
                is_parsed = False
            elif game_manager.is_in_map:
                if not is_parsed:
                    nb_drone, hubs, connexions, map_instance = simu_init(
                        maps_path[difficulty_select.selection_state][
                            map_select.selection_state
                        ]
                    )

                    if map_instance is None:
                        raise ValueError("Error during map creation!")
                    if not map_instance.start_ok:
                        raise ValueError("multiple start!")
                    if not map_instance.end_ok:
                        raise ValueError("multiple end!")

                    occupancy: defaultdict[tuple[Any, ...], int] = defaultdict(
                        int
                    )

                    if nb_drone:
                        map_instance.start.current_nb_drone = nb_drone
                    for d in map_instance.drones:
                        d.define_start_position(hubs, vizualizer)
                        d.current_position = d.start_position.copy()
                        d.dijsktra(map_instance, occupancy)

                    print_simulation(
                        map_instance.drones, map_instance.start.name
                    )
                    is_parsed = True

                vizualizer.draw_loop(
                    map_instance,
                    difficulty_select.selection_state,
                    map_select.selection_state,
                )
                mouse_hover(vizualizer, hubs)

                play_simulation(game_manager, map_instance, vizualizer)

            read_input(
                game_manager,
                main_menu_manager,
                difficulty_select,
                map_select,
                map_instance,
                vizualizer,
            )
            vizualizer.update()
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)
