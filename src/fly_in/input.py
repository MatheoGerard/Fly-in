import pygame as pg


def read_user_input():
    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                elif event.key == pg.K_SPACE:
                    pg.display.toggle_fullscreen()

                else:
                    print(event.key)
