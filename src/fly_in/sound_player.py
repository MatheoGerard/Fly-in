import pygame as pg


def play_sound_assets(index_sound: int) -> None:
    match index_sound:
        case 1:
            pg.mixer.music.load("sound/05. Last Mission.mp3")  # medium music
            pg.mixer.music.play()
        case 0:
            pg.mixer.music.load("sound/08. Space Adventure.mp3")  # music easy
            pg.mixer.music.play()
        case 2:
            pg.mixer.music.load("sound/10. Jester Theme.mp3")  # hard music
            pg.mixer.music.play()
        case 4:
            pg.mixer.music.load("sound/04. Mechanical Complex.mp3")  # menu music
            pg.mixer.music.play()
        case 3:
            pg.mixer.music.load("sound/15. Rush Point.mp3")  # challenger music
            pg.mixer.music.play()
