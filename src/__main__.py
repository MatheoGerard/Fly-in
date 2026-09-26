import pygame as pg
from fly_in import Visualization as vizu
from fly_in import Parser
from fly_in import Map

if __name__ == "__main__":
    pars = Parser(file_name="maps/hard/03_ultimate_challenge.txt")
    content = pars.read_map_file()
    hubs = pars.create_hub(content)
    connexions = pars.create_connexion(content, hubs)
    for co in connexions:
        print(co.max_link_capacity)

    map_instance: Map = Map(pars.find_nb_drones(content), hubs)

    if not map_instance.start_ok:
        raise ValueError("multiple start!")
    if not map_instance.end_ok:
        raise ValueError("multiple end!")

    pg.init()

    circle_pos = [300, 300]
    vizualizer = vizu()
    vizualizer.create_window()
    vizualizer.draw_connexions(connexions, hubs)
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
                        pg.display.toggle_fullscreen()  # FIXME: probleme a la sortie du full screen!
                    case _:
                        print(event.key)
