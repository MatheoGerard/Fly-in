import pygame as pg
from fly_in import Visualization as vizu
from fly_in import (
    Parser,
    Map,
    read_input,
    GameState,
    MainMenu,
    SelectionDif,
    SelectionMap,
)


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


if __name__ == "__main__":
    maps_path: list[list[str]] = load_maps()

    pg.init()
    game_manager = GameState()
    main_menu_manager: MainMenu = MainMenu(
        "textures/backrgound/PO_main_background.bmp", game_manager, 2
    )
    main_menu_manager.create_button()
    difficulty_select = SelectionDif()
    map_select = SelectionMap()
    vizualizer = vizu()
    vizualizer.create_window()

    while game_manager.game_running:
        if game_manager.is_main_menu:
            vizualizer.draw_main_menu(main_menu_manager, True)
        elif game_manager.is_difficulty_select:
            vizualizer.draw_select_dif(difficulty_select, True)
        elif game_manager.is_map_selection:
            vizualizer.draw_select_map(difficulty_select, map_select)
        elif game_manager.is_in_map:
            pars = Parser(
                file_name=maps_path[difficulty_select.selection_state][
                    map_select.selection_state
                ]
            )
            content = pars.read_map_file()
            hubs = pars.create_hub(content)
            connexions = pars.create_connexion(content, hubs)

            map_instance: Map = Map(pars.find_nb_drones(content), hubs)

            if not map_instance.start_ok:
                raise ValueError("multiple start!")
            if not map_instance.end_ok:
                raise ValueError("multiple end!")
            vizualizer.draw_background()
            vizualizer.draw_connexions(connexions, hubs)
            vizualizer.draw_hub(hubs)

        vizualizer.update()
        read_input(
            game_manager, main_menu_manager, difficulty_select, map_select
        )
