"""
Music playback helpers.
"""

import pygame as pg


def play_sound_assets(index_sound: int) -> None:
    """
    Load and play the music matching an index.

    Args:
        index_sound: Index of the music: 0 for Space Adventure, 1 for Last
            Mission, 2 for Jester Theme, 3 for Rush Point and 4 for Mechanical
            Complex.
    """
    match index_sound:
        case 1:
            pg.mixer.music.load("sound/05. Last Mission.mp3")
            pg.mixer.music.play()
        case 0:
            pg.mixer.music.load("sound/08. Space Adventure.mp3")
            pg.mixer.music.play()
        case 2:
            pg.mixer.music.load("sound/10. Jester Theme.mp3")
            pg.mixer.music.play()
        case 4:
            pg.mixer.music.load("sound/04. Mechanical Complex.mp3")
            pg.mixer.music.play()
        case 3:
            pg.mixer.music.load("sound/15. Rush Point.mp3")
            pg.mixer.music.play()
