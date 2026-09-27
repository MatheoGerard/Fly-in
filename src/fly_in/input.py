import pygame as pg
from .game_state import GameState


def read_input(game_manager: GameState) -> None:
    events = pg.event.get()

    for event in events:
        if event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_ESCAPE:
                    exit()
                case pg.K_SPACE:
                    pg.display.toggle_fullscreen()  # FIXME: probleme a la sortie du full screen!
                case _:
                    print(event.key)
