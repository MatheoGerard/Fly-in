import pygame as pg


def create_window():
    screen = pg.display.set_mode((1920, 1080))
    pg.display.set_caption("Fly-In")

    screen.fill((30, 30, 30))
    pg.display.flip()

    return screen


def draw_circle(screen, x, y) -> pg.rect.Rect:
    return pg.draw.circle(screen, (255, 255, 255), (x, y), 100)
