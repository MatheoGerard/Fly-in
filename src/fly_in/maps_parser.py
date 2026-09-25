import parse
from pydantic import BaseModel
from .hub import hub
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

    def parse_meta(self, meta: str) -> dict[str, str] | None:
        meta_parsed: dict[str, str] = {
            "color": "none",
            "max_drones": "1",
            "zone": "normal",
        }

        if not meta:
            return meta_parsed

        if "color=" in meta:
            meta_parsed["color"] = parse.search("color={:w}", meta).fixed[0]
        if "zone=" in meta:
            meta_parsed["zone"] = parse.search("zone={:w}", meta).fixed[0]
        if "max_drones=" in meta:
            meta_parsed["max_drones"] = parse.search(
                "max_drones={:w}", meta
            ).fixed[0]

        return meta_parsed

    def find_nb_drones(self, content) -> int | None:
        for line in content:
            if line.strip().startswith("nb_drones: "):
                return int(parse.search("nb_drones: {:d}", line).fixed[0])

        return None

    def create_hub(self, content: str) -> list[hub]:
        hubs: list[hub] = []
        base: str = ""
        meta: str = ""

        mandatory = None
        optionnal: dict[str, str] | None
        optionnal = self.parse_meta(meta.strip("[]"))

        for line in content.splitlines():
            if line.strip().startswith("#"):
                continue

            elif line.strip().startswith("end_hub: "):
                if "[" in line:
                    base, meta = line.split("[")
                else:
                    base = line
                mandatory = parse.parse(
                    "end_hub: {:w} {:d} {:d}", base.strip()
                )
                if meta:
                    optionnal = self.parse_meta(meta.strip("[]"))

                new_hub: hub = hub(
                    name=mandatory[0],
                    position=(mandatory[1], mandatory[2]),
                    zone_type=optionnal.get("zone"),
                    color=optionnal.get("color"),
                    max_drone=optionnal.get("max_drones"),
                    state=2,
                )
                hubs.append(new_hub)

            elif line.strip().startswith("start_hub: "):
                if "[" in line:
                    base, meta = line.split("[")
                else:
                    base = line
                mandatory = parse.parse(
                    "start_hub: {:w} {:d} {:d}", base.strip()
                )
                if meta:
                    optionnal = self.parse_meta(meta.strip("[]"))

                new_hub: hub = hub(
                    name=mandatory[0],
                    position=(mandatory[1], mandatory[2]),
                    zone_type=optionnal.get("zone"),
                    color=optionnal.get("color"),
                    max_drone=optionnal.get("max_drones"),
                    state=0,
                )
                hubs.append(new_hub)

            elif line.strip().startswith("hub: "):
                if "[" in line:
                    base, meta = line.split("[")
                else:
                    base = line
                mandatory = parse.parse("hub: {:w} {:d} {:d}", base.strip())
                if meta:
                    optionnal = self.parse_meta(meta.strip("[]"))

                new_hub: hub = hub(
                    name=mandatory[0],
                    position=(mandatory[1], mandatory[2]),
                    zone_type=optionnal.get("zone"),
                    color=optionnal.get("color"),
                    max_drone=optionnal.get("max_drones"),
                    state=1,
                )
                hubs.append(new_hub)

        return hubs

    def create_connexion(
        self, content: str, hubs: list[hub]
    ) -> list[Connexion]:
        connexions: list[Connexion] = []

        for line in content.splitlines():
            if line.strip().startswith("connection: "):
                points = parse.parse("connection: {:w}-{:w}", line)
                print(points)
            else:
                continue

            hubs_to_connected = []

            if points:
                for point in points:
                    for hub in hubs:
                        if point == hub.name:
                            hubs_to_connected.append(hub)
                new_connexion = Connexion(
                    hubs_to_connected[0], hubs_to_connected[1]
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
