import parse
from pydantic import BaseModel
from .hub import Hub
from .connexion import Connexion


class Parser(BaseModel):
    file_name: str

    def read_map_file(self) -> str:
        try:
            with open(self.file_name, "r") as file:
                return file.read()
        except PermissionError as e:
            print(e)
            return ""
        except FileNotFoundError as e:
            print(e)
            return ""
        except Exception as e:
            print(e)
            return ""

    def parse_meta(self, meta: str) -> dict[str, str]:
        meta_parsed: dict[str, str] = {
            "color": "none",
            "max_drones": "1",
            "zone": "normal",
        }

        if not meta:
            return meta_parsed

        for word in meta.split(" "):
            if word.split("=")[0] not in meta_parsed.keys():
                raise ValueError(
                    f"{word.split('=')[0]} is not a valid meta data!"
                )

        if "color=" in meta:
            meta_parsed["color"] = parse.search("color={:w}", meta).fixed[0]
        if "zone=" in meta:
            meta_parsed["zone"] = parse.search("zone={:w}", meta).fixed[0]
        if "max_drones=" in meta:
            meta_parsed["max_drones"] = parse.search(
                "max_drones={:d}", meta
            ).fixed[0]

        return meta_parsed

    def find_nb_drones(self, content: str) -> int | None:
        for line in content.splitlines():
            if line.strip().startswith("#") or not line.replace(" ", ""):
                continue
            if line.startswith("nb_drones: "):
                return int(parse.search("nb_drones: {:d}", line).fixed[0])
            else:
                raise ValueError(
                    "definition of nb_drones must ne the very first line!"
                )

        return None

    def create_hub(self, content: str) -> list[Hub]:
        hubs: list[Hub] = []
        base: str = ""
        meta: str = ""

        mandatory = None
        optionnal: dict[str, str]
        optionnal = self.parse_meta(meta.strip("[]"))

        for line in content.splitlines():
            meta = ""
            optionnal = self.parse_meta("")

            if line.strip().startswith("#"):
                continue

            elif line.strip().startswith("end_hub: "):
                if "[" in line:
                    base, meta = line.split("[")
                else:
                    base = line
                mandatory = parse.parse(
                    "end_hub: {:S} {:d} {:d}", base.strip()
                )
                if meta:
                    optionnal = self.parse_meta(meta.strip("[]"))

                new_hub: Hub = Hub(
                    name=mandatory[0],
                    position=[mandatory[1], -mandatory[2]],
                    zone_type=optionnal["zone"],
                    color=optionnal["color"],
                    max_drone=int(optionnal["max_drones"]),
                    state=2,
                )
                hubs.append(new_hub)

            elif line.strip().startswith("start_hub: "):
                if "[" in line:
                    base, meta = line.split("[")
                else:
                    base = line
                mandatory = parse.parse(
                    "start_hub: {:S} {:d} {:d}", base.strip()
                )
                if meta:
                    optionnal = self.parse_meta(meta.strip("[]"))

                new_hub = Hub(
                    name=mandatory[0],
                    position=[mandatory[1], -mandatory[2]],
                    zone_type=optionnal["zone"],
                    color=optionnal["color"],
                    max_drone=int(optionnal["max_drones"]),
                    state=0,
                )
                hubs.append(new_hub)

            elif line.strip().startswith("hub: "):
                if "[" in line:
                    base, meta = line.split("[")
                else:
                    base = line
                mandatory = parse.parse("hub: {:S} {:d} {:d}", base.strip())
                if mandatory is None:
                    raise ValueError(
                        "hub line  must be at least 'hub: <name> <x> <y> "
                        "([meta_data...])'"
                    )
                if meta:
                    optionnal = self.parse_meta(meta.strip("[]"))

                new_hub = Hub(
                    name=mandatory[0],
                    position=[mandatory[1], -mandatory[2]],
                    zone_type=optionnal["zone"],
                    color=optionnal["color"],
                    max_drone=int(optionnal["max_drones"]),
                    state=1,
                )
                hubs.append(new_hub)

        return hubs

    def create_connexion(
        self, content: str, hubs: list[Hub]
    ) -> list[Connexion]:
        connexions: list[Connexion] = []
        base: str = ""
        meta_link: str = ""
        link_capacity: int

        for line in content.splitlines():
            link_capacity = 1
            meta_link = ""
            if line.strip().startswith("connection: "):
                if "[" in line:
                    base, meta_link = line.split("[")
                else:
                    base = line

                if meta_link:
                    if (
                        meta_link.strip("[]").split("=")[0]
                        != "max_link_capacity"
                    ):
                        raise ValueError(
                            "max_link_capacity must be define with "
                            "'max_link_capacity=...'"
                        )
                    link_capacity = parse.search(
                        "max_link_capacity={:d}", meta_link.strip("[]")
                    ).fixed[0]

                points = parse.parse("connection: {:S}-{:S}", base.strip())

                hubs_to_connected = []

                if points:
                    for point in points:
                        for hub in hubs:
                            if point == hub.name:
                                hubs_to_connected.append(hub)
                    if len(hubs_to_connected) > 2:
                        raise ValueError("Multiple hubs have the same name!")

                    if len(hubs_to_connected) != 2:
                        raise ValueError(
                            "Impossible to create a connexion between"
                            " hubs not exist"
                        )
                    new_connexion = Connexion(
                        a=hubs_to_connected[0],
                        b=hubs_to_connected[1],
                        max_link_capacity=link_capacity,
                    )
                    connexions.append(new_connexion)
                    hubs_to_connected.clear()

        return connexions


if __name__ == "__main__":
    try:
        parser = Parser(file_name="maps/easy/01_linear_path.txt")

        content: str = parser.read_map_file()
        new = parser.create_hub(content)
    except Exception as e:
        print(e)
