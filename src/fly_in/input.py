import pygame as pg

from .display import Visualization as visu
from .hub import hub
from .main_menu import MainMenu, SelectionDif, SelectionMap
from .game_state import GameState
from .map_class import Map


def mouse_hover(dis: visu, hubs: list[hub]) -> None:
    offset_x, offset_y = dis.find_true_positions(hubs)
    sub_value_x = min(hub.position[0] for hub in hubs)
    sub_value_y = min(hub.position[1] for hub in hubs)

    for points in hubs:
        if (
            points.get_true_x(sub_value_x, offset_x) - 25
            <= pg.mouse.get_pos()[0]
            and points.get_true_x(sub_value_x, offset_x) + 25
            >= pg.mouse.get_pos()[0]
        ):
            if (
                points.get_true_y(sub_value_y, offset_y) - 25
                <= pg.mouse.get_pos()[1]
                and points.get_true_y(sub_value_y, offset_y) + 25
                >= pg.mouse.get_pos()[1]
            ):
                dis.draw_hub_name(
                    points,
                    [
                        points.get_true_x(sub_value_x, offset_x),
                        points.get_true_y(sub_value_y, offset_y),
                    ],
                )


def read_input(
    game_manager: GameState,
    main_menu_manager: MainMenu,
    dif_select_manager: SelectionDif,
    map_selector: SelectionMap,
    map_instance: Map,
    visu,
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
                        map_selector.change_selection(-1, dif_select_manager)
                    elif game_manager.is_in_map:
                        if map_instance:
                            for d in map_instance.drones:
                                d.move(map_instance.hubs, visu, map_instance)
                                d.find_way(d.current_hub)
                case pg.K_UP:
                    if game_manager.is_main_menu:
                        main_menu_manager.change_selection(1)
                    elif game_manager.is_difficulty_select:
                        dif_select_manager.change_selection(1)
                    elif game_manager.is_map_selection:
                        map_selector.change_selection(1, dif_select_manager)
                    elif game_manager.is_in_map:
                        if map_instance:
                            for d in map_instance.drones:
                                d.find_way(d.current_hub)
                                d.move(map_instance.hubs, visu, map_instance)
                case pg.K_RETURN:
                    if game_manager.is_main_menu:
                        if main_menu_manager.selection_state == 1:
                            exit()
                        game_manager.set_main_menu()
                        game_manager.set_difficulty_select()
                    elif game_manager.is_difficulty_select:
                        game_manager.set_difficulty_select()
                        game_manager.set_map_selector()
                    elif game_manager.is_map_selection:
                        game_manager.set_map_selector()
                        game_manager.set_in_map()
                case pg.K_ESCAPE:
                    if game_manager.is_difficulty_select:
                        game_manager.set_difficulty_select()
                        game_manager.set_main_menu()
                    elif game_manager.is_map_selection:
                        map_selector.selection_state = 0
                        game_manager.set_map_selector()
                        game_manager.set_difficulty_select()
                    elif game_manager.is_in_map:
                        map_selector.selection_state = 0
                        game_manager.set_in_map()
                        game_manager.set_map_selector()
                case pg.K_SPACE:
                    pg.display.toggle_fullscreen()
                case _:
                    print(event.key)
