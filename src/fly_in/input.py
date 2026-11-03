"""
Keyboard and mouse input handling.
"""

import pygame as pg
from .display import Visualization
from .hub import Hub
from .main_menu import MainMenu, SelectionDif, SelectionMap
from .game_state import GameState
from .map_class import Map


def mouse_hover(dis: Visualization, hubs: list[Hub]) -> None:
    """
    Draw the name of the hub hovered by the mouse cursor.

    Args:
        dis: Visualization used to draw the name.
        hubs: Hubs of the map.
    """
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


def space_input() -> None:
    """
    Toggle the fullscreen mode.
    """
    pg.display.toggle_fullscreen()


def escape_input(
    game_manager: GameState,
    map_selector: SelectionMap,
    dif_select_manager: SelectionDif,
) -> None:
    """
    Go back to the previous screen.

    From the difficulty selection the main menu is shown, from the map
    selection the difficulty selection is shown and from a map the map
    selection is shown.

    Args:
        game_manager: State of the game.
        map_selector: Map selection, reset to its first map.
        dif_select_manager: Difficulty selection.
    """
    if game_manager.is_difficulty_select:
        game_manager.set_difficulty_select()
        game_manager.set_main_menu()
    elif game_manager.is_map_selection:
        map_selector.selection_state = 0
        game_manager.set_map_selector(dif_select_manager.selection_state)
        game_manager.set_difficulty_select()
    elif game_manager.is_in_map:
        map_selector.selection_state = 0
        game_manager.set_in_map()
        game_manager.set_map_selector(
            dif_select_manager.selection_state, False
        )


def return_input(
    game_manager: GameState,
    main_menu_manager: MainMenu,
    dif_select_manager: SelectionDif,
) -> None:
    """
    Validate the current choice and go to the next screen.

    The program exits if the quit button of the main menu is selected.

    Args:
        game_manager: State of the game.
        main_menu_manager: Main menu.
        dif_select_manager: Difficulty selection.
    """
    if game_manager.is_main_menu:
        if main_menu_manager.selection_state == 1:
            exit()
        game_manager.set_main_menu()
        game_manager.set_difficulty_select()
    elif game_manager.is_difficulty_select:
        game_manager.set_difficulty_select()
        game_manager.set_map_selector(dif_select_manager.selection_state)
    elif game_manager.is_map_selection:
        game_manager.set_map_selector(dif_select_manager.selection_state)
        game_manager.set_in_map()


def p_input(game_manager: GameState) -> None:
    """
    Toggle the play mode if a map is displayed.

    Args:
        game_manager: State of the game.
    """
    if game_manager.is_in_map:
        game_manager.set_play_mode()


def read_input(
    game_manager: GameState,
    main_menu_manager: MainMenu,
    dif_select_manager: SelectionDif,
    map_selector: SelectionMap,
    map_instance: Map | None,
    visu: Visualization,
) -> None:
    """
    Handle the keyboard events of the current frame.

    P toggles the play mode, the up and down arrows change the selection (or
    play a step in a map), Enter validates, Escape goes back and Space toggles
    the fullscreen. Any other key is printed.

    Args:
        game_manager: State of the game.
        main_menu_manager: Main menu.
        dif_select_manager: Difficulty selection.
        map_selector: Map selection.
        map_instance: Current map, or None if no map is loaded.
        visu: Visualization used to move the drones.
    """
    events = pg.event.get()

    for event in events:
        if event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_p:
                    p_input(game_manager)
                case pg.K_DOWN:
                    if game_manager.is_main_menu:
                        main_menu_manager.change_selection(1)
                    elif game_manager.is_difficulty_select:
                        dif_select_manager.change_selection(-1)
                    elif game_manager.is_map_selection:
                        map_selector.change_selection(-1, dif_select_manager)
                    elif (
                        game_manager.is_in_map
                        and not game_manager.is_play_mode
                    ):
                        if map_instance:
                            for d in map_instance.drones:
                                d.move(map_instance.hubs, visu, map_instance)
                case pg.K_UP:
                    if game_manager.is_main_menu:
                        main_menu_manager.change_selection(1)
                    elif game_manager.is_difficulty_select:
                        dif_select_manager.change_selection(1)
                    elif game_manager.is_map_selection:
                        map_selector.change_selection(1, dif_select_manager)
                    elif (
                        game_manager.is_in_map
                        and not game_manager.is_play_mode
                    ):
                        if map_instance:
                            map_instance.turn += 1
                            for d in map_instance.drones:
                                d.move(map_instance.hubs, visu, map_instance)
                case pg.K_RETURN:
                    return_input(
                        game_manager, main_menu_manager, dif_select_manager
                    )
                case pg.K_ESCAPE:
                    escape_input(
                        game_manager, map_selector, dif_select_manager
                    )
                case pg.K_SPACE:
                    space_input()
                case _:
                    print(event.key)
