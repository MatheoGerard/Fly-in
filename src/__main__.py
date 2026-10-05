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

if __name__ == "__main__":
    pars = Parser(file_name="maps/hard/03_ultimate_challenge.txt")
    content = pars.read_map_file()
    hubs = pars.create_hub(content)
    connexions = pars.create_connexion(content, hubs)

    map_instance: Map = Map(pars.find_nb_drones(content), hubs)

    if not map_instance.start_ok:
        raise ValueError("multiple start!")
    if not map_instance.end_ok:
        raise ValueError("multiple end!")

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
        else:
            vizualizer.draw_background()
            vizualizer.draw_connexions(connexions, hubs)
            vizualizer.draw_hub(hubs)

        vizualizer.update()
        read_input(game_manager, main_menu_manager, difficulty_select)
