from .hub import hub as Hub
from .maps_parser import Parser
from .connexion import Connexion
from .map_class import Map


def simu_init(
    file_name: str,
) -> tuple[int | None, list[Hub], list[Connexion], Map]:
    pars: Parser = Parser(file_name=file_name)

    content: str = pars.read_map_file()
    nb_drone: int | None = pars.find_nb_drones(content)
    hubs: list[Hub] = pars.create_hub(content)
    connexions: list[Connexion] = pars.create_connexion(content, hubs)

    if nb_drone:
        map_instance: Map = Map(nb_drone, hubs, connexions)

    for hub in hubs:
        hub.define_cost()

    return (nb_drone, hubs, connexions, map_instance)
