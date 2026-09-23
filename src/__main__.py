import pygame as pg
import fly_in

if __name__ == "__main__":
    pg.init()

    circle_pos = [300, 300]
    screen = fly_in.create_window()
    fly_in.draw_circle(screen, circle_pos[0], circle_pos[1])
    pg.display.flip()

    while True:
        events = pg.event.get()

        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_ESCAPE:
                        exit()
                    case pg.K_SPACE:
                        pg.display.toggle_fullscreen()
                    case _:
                        print(event.key)

        screen.fill((30, 30, 30))
        circle_pos[0] += 1
        fly_in.draw_circle(screen, circle_pos[0], circle_pos[1])
        pg.display.flip()
