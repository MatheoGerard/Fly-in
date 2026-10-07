import pygame as pg

from .main_menu import MainMenu, SelectionDif, SelectionMap
from .game_state import GameState


def read_input(
    game_manager: GameState,
    main_menu_manager: MainMenu,
    dif_select_manager: SelectionDif,
    map_selector: SelectionMap,
) -> None:
    events = pg.event.get()

    for event in events:
        if event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_DOWN:
                    if game_manager.is_main_menu:
                        main_menu_manager.change_selection(1)
                    elif game_manager.is_difficulty_select:
                        dif_select_manager.change_selection(-1)
                    elif game_manager.is_map_selection:
                        map_selector.change_selection(-1)
                case pg.K_UP:
                    if game_manager.is_main_menu:
                        main_menu_manager.change_selection(1)
                    elif game_manager.is_difficulty_select:
                        dif_select_manager.change_selection(1)
                    elif game_manager.is_map_selection:
                        map_selector.change_selection(1)
                case pg.K_RETURN:
                    if game_manager.is_main_menu:
                        if main_menu_manager.selection_state == 1:
                            exit()
                        game_manager.set_main_menu()
                        game_manager.set_difficulty_select()
                    elif game_manager.is_difficulty_select:
                        game_manager.set_difficulty_select()
                        game_manager.set_map_selector()
                case pg.K_ESCAPE:
                    if game_manager.is_difficulty_select:
                        game_manager.set_difficulty_select()
                        game_manager.set_main_menu()
                case pg.K_SPACE:
                    pg.display.toggle_fullscreen()  # FIXME: probleme a la sortie du full screen!
                case _:
                    print(event.key)
