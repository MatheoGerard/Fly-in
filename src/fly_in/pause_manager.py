import pygame as pg
from .game_state import GameState
from fly_in import game_state


def paused(game_manager: GameState) -> None:
    game_manager.set_paused()
