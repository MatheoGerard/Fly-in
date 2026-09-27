import pygame as pg

from .main_menu import MainMenu
from .game_state import GameState


def read_input(game_manager: GameState, main_menu_manager: MainMenu) -> None:
    events = pg.event.get()

    for event in events:
        if event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_DOWN:
                    main_menu_manager.change_selection(1)
                case pg.K_UP:
                    main_menu_manager.change_selection(-1)
                case pg.K_RETURN:
                    if main_menu_manager.selection_state == 1:
                        exit()
                    game_manager.set_main_menu()
                case pg.K_ESCAPE:
                    exit()
                case pg.K_SPACE:
                    pg.display.toggle_fullscreen()  # FIXME: probleme a la sortie du full screen!
                case _:
                    print(event.key)
