import pygame as pg
from fly_in import Visualization as vizu, drone
from fly_in import (
    Parser,
    Map,
    read_input,
    GameState,
    MainMenu,
    SelectionDif,
    SelectionMap,
    mouse_hover,
)
from fly_in.connexion import Connexion


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
    hubs = []

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
                pars = Parser(
                    file_name=maps_path[difficulty_select.selection_state][
                        map_select.selection_state
                    ]
                )
                content = pars.read_map_file()
                nb_drone = pars.find_nb_drones(content)
                hubs = pars.create_hub(content)

                for hub in hubs:
                    hub.define_cost()

                connexions = pars.create_connexion(content, hubs)

                map_instance = Map(nb_drone, hubs, connexions)
                map_instance.finish.max_drone = 999999999999999999999999999999
                print(f"finish: {map_instance.finish.name}", flush=True)

                for d in map_instance.drones:
                    print("coucou")
                    d.define_start_position(hubs, vizualizer)
                    d.current_position = d.start_position
                    d.dijsktra(map_instance)

                if not map_instance.start_ok:
                    raise ValueError("multiple start!")
                if not map_instance.end_ok:
                    raise ValueError("multiple end!")

                is_parsed = True

            vizualizer.draw_background()
            vizualizer.draw_connexions(connexions, hubs)
            vizualizer.draw_hub(hubs)
            vizualizer.draw_drones(map_instance.drones)
            mouse_hover(vizualizer, hubs)

        read_input(
            game_manager,
            main_menu_manager,
            difficulty_select,
            map_select,
            map_instance,
            vizualizer,
        )
        vizualizer.update()
