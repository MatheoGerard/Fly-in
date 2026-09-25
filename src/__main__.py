import pygame as pg
from fly_in import Visualization as vizu
from fly_in import Parser

if __name__ == "__main__":
    try:
        pars = Parser(file_name="maps/easy/01_linear_path.txt")
        content = pars.read_map_file()
        hubs = pars.create_hub(content)

        pg.init()

        circle_pos = [300, 300]
        vizualizer = vizu()
        vizualizer.create_window()
        vizualizer.draw_hub(hubs)
        vizualizer.update()

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

    except Exception as e:
        print(e)
