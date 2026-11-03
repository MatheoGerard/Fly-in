"""
Parser of the map files.
"""

import parse
from pydantic import BaseModel
from .hub import Hub
from .connexion import Connexion


class Parser(BaseModel):
    """
    Parse a map file into hubs and connections.

    Attributes:
        file_name: Path of the map file.
    """

    file_name: str

    def read_map_file(self) -> str:
        """
        Read the map file.

        Returns:
            The content of the file, or an empty string if it cannot be read
            (the error is printed).
        """
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
        """
        Parse the metadata of a hub.

        Args:
            meta: Metadata without brackets, for example ``color=red
                zone=priority max_drones=2``.

        Returns:
            A dictionary with the keys ``color``, ``max_drones`` and ``zone``,
            filled with default values for missing metadata.

        Raises:
            ValueError: If a metadata name is not valid.
        """
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
        """
        Find the number of drones defined in the map file.

        Args:
            content: Content of the map file.

        Returns:
            The number of drones, or None if the file has no meaningful line.

        Raises:
            ValueError: If the first meaningful line is not ``nb_drones:
                <value>`` or if the value is not valid.
        """
        for line in content.splitlines():
            if line.strip().startswith("#") or not line.replace(" ", ""):
                continue
            if line.startswith("nb_drones: "):
                try:
                    return int(parse.search("nb_drones: {:S}", line).fixed[0])
                except Exception:
                    raise ValueError("nb_drone not a valid value")
            else:
                raise ValueError(
                    "definition of nb_drones must be the very first line!"
                )

        return None

    def create_hub(self, content: str) -> list[Hub]:
        """
        Create the hubs defined in the map file.

        The ``start_hub``, ``hub`` and ``end_hub`` lines are parsed. Comment
        lines are ignored.

        Args:
            content: Content of the map file.

        Returns:
            The list of created hubs.

        Raises:
            ValueError: If a line, its position or its metadata is not valid.
        """
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
                    "end_hub: {:S} {:S} {:S}", base.strip()
                )
                if mandatory is None:
                    raise ValueError(
                        "hub line  must be at least 'hub: <name> <x> <y> "
                        "([meta_data...])'"
                    )
                try:
                    int(mandatory[1])
                except Exception:
                    raise ValueError(
                        f"'{mandatory[1]}' is not a valid value"
                        " for a position x"
                    )
                try:
                    int(mandatory[2])
                except Exception:
                    raise ValueError(
                        f"'{mandatory[2]}' is not a valid value"
                        " for a position y"
                    )
                if meta:
                    meta_clean = "["
                    for c in meta:
                        if c == "[" or c == "]":
                            meta_clean += c
                    if meta_clean != "[]":
                        raise ValueError(
                            f"'[{meta}' is not in a valid syntax!"
                        )
                    optionnal = self.parse_meta(meta.strip("[]"))

                new_hub: Hub = Hub(
                    name=mandatory[0],
                    position=[int(mandatory[1]), -int(mandatory[2])],
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
                    "start_hub: {:S} {:S} {:S}", base.strip()
                )
                if mandatory is None:
                    raise ValueError(
                        "hub line  must be at least 'hub: <name> <x> <y> "
                        "([meta_data...])'"
                    )
                try:
                    int(mandatory[1])
                except Exception:
                    raise ValueError(
                        f"'{mandatory[1]}' is not a valid"
                        " value for a position x"
                    )
                try:
                    int(mandatory[2])
                except Exception:
                    raise ValueError(
                        f"'{mandatory[2]}' is not a valid"
                        " value for a position y"
                    )
                if meta:
                    meta_clean = "["
                    for c in meta:
                        if c == "[" or c == "]":
                            meta_clean += c
                    if meta_clean != "[]":
                        raise ValueError(
                            f"'[{meta}' is not in a valid syntax!"
                        )
                    optionnal = self.parse_meta(meta.strip("[]"))

                new_hub = Hub(
                    name=mandatory[0],
                    position=[int(mandatory[1]), -int(mandatory[2])],
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
                mandatory = parse.parse("hub: {:S} {:S} {:S}", base.strip())
                if mandatory is None:
                    raise ValueError(
                        "hub line  must be at least 'hub: <name> <x> <y> "
                        "([meta_data...])'"
                    )
                try:
                    int(mandatory[1])
                except Exception:
                    raise ValueError(
                        f"'{mandatory[1]}' is not a valid value"
                        " for a position x"
                    )
                try:
                    int(mandatory[2])
                except Exception:
                    raise ValueError(
                        f"'{mandatory[2]}' is not a valid value"
                        " for a position y"
                    )
                if meta:
                    meta_clean = "["
                    for c in meta:
                        if c == "[" or c == "]":
                            meta_clean += c
                    if meta_clean != "[]":
                        raise ValueError(
                            f"'[{meta}' is not in a valid syntax!"
                        )
                    optionnal = self.parse_meta(meta.strip("[]"))

                new_hub = Hub(
                    name=mandatory[0],
                    position=[int(mandatory[1]), -int(mandatory[2])],
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
        """
        Create the connections defined in the map file.

        Each ``connection`` line links two existing hubs and may set
        ``max_link_capacity``.

        Args:
            content: Content of the map file.
            hubs: Hubs the connections refer to.

        Returns:
            The list of created connections.

        Raises:
            ValueError: If the metadata or the link capacity is not valid, if
                several hubs share a name or if a hub does not exist.
        """
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
                    meta_clean = "["
                    for c in meta_link:
                        if c == "[" or c == "]":
                            meta_clean += c
                    if meta_clean != "[]":
                        raise ValueError(
                            f"'[{meta_link}' is not in a valid syntax!"
                        )
                    if (
                        meta_link.strip("[]").split("=")[0]
                        != "max_link_capacity"
                    ):
                        raise ValueError(
                            "max_link_capacity must be define with "
                            "'max_link_capacity=...'"
                        )
                    link_capacity = parse.search(
                        "max_link_capacity={:S}", meta_link.strip("[]")
                    ).fixed[0]
                    try:
                        int(link_capacity)
                    except Exception:
                        raise ValueError(
                            f"{link_capacity} is not a valid value"
                            " for a max_link_capacity"
                        )

                points = parse.parse("connection: {:S}-{:S}", base.strip())

                hubs_to_connected = []

                if not points:
                    raise ValueError(
                        f"'{line}' is not a valid definition of a connection"
                    )

                if points:
                    for point in points:
                        for hub in hubs:
                            if point == hub.name:
                                hubs_to_connected.append(hub)
                    if len(hubs_to_connected) > 2:
                        raise ValueError("Multiple hubs have the same name!")

                    if len(hubs_to_connected) != 2:
                        raise ValueError(
                            "Impossible to create a connexion"
                            " between hubs not exist"
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
