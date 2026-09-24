import parse
from pydantic import BaseModel, PositiveFloat
from hub import hub


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

    def create_hub(self, content: str) -> list[hub]:
        hubs: list[hub] = []
        base: str = ""
        meta: str = ""

        mandatory = None
        optionnal: dict[str, str] | None
        optionnal = self.parse_meta(meta.strip("[]"))

        for line in content.splitlines():
            if line.strip().startswith("hub: "):
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
                )
                hubs.append(new_hub)

        for hub_obj in hubs:
            print(hub_obj.name, end=" ")
            print(hub_obj.position, end=" ")
            print(hub_obj.zone_type, end=" ")
            print(hub_obj.color, end=" ")
            print(hub_obj.max_drone)

        return hubs


if __name__ == "__main__":
    parser = Parser(file_name="maps/easy/01_linear_path.txt")

    content: str = parser.read_map_file()
    new = parser.create_hub(content)
