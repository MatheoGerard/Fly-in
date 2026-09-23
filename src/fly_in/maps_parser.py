import parse
from pydantic import BaseModel
from .hub import hub


class Parser(BaseModel):
    file_name: str
    data_file: str

    def read_map_file(self) -> None:
        try:
            with open(self.file_name, "r") as file:
                self.data_file = file.read()
        except PermissionError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(e)

    def create_hub(self) -> list[hub]:
        hubs: list[hub] = []

        for line in self.data_file:
            if line.strip().startswith("hub: "):
                new_hub: hub = hub()
