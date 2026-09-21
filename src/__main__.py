from time import sleep
import pygame as pg
import fly_in

if __name__ == "__main__":
    pg.init()

    circle_pos = [300, 300]
    screen = fly_in.create_window()
    fly_in.draw_circle(screen, circle_pos[0], circle_pos[1])
    pg.display.flip()

    for _ in range(0, 10):
        screen.fill((30, 30, 30))
        circle_pos[0] += 10
        fly_in.draw_circle(screen, circle_pos[0], circle_pos[1])
        pg.display.flip()
        sleep(1)

    fly_in.read_user_input()
