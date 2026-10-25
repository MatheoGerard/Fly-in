from __future__ import annotations

from pygame import Color
from pydantic import BaseModel, model_validator


class hub(BaseModel):
    name: str
    position: list[int]

    zone_type: str
    color: str
    max_drone: int
    state: int

    neighbor: list[hub] = []
    cost: float = 0
    current_nb_drone: int = 0
    visited: bool = False

    def define_cost(self) -> None:
        match self.zone_type:
            case "blocked":
                self.cost = float("inf")
            case "restricted":
                self.cost = 2.0
            case "priority":
                self.cost = 0.999999
            case _:
                self.cost = 1.0

    def get_color(self) -> Color | str:
        if self.color == "none" or self.color == "rainbow":
            return Color("aqua")

        return Color(self.color)

    def get_true_x(self, sub_value, offset_x) -> int:
        return (self.position[0] - sub_value + 1) * offset_x

    def get_true_y(self, sub_value, offset_y) -> int:
        return (self.position[1] - sub_value + 1) * offset_y

    def update_current_nb_drone(self, change_value: int) -> None:
        self.current_nb_drone += change_value

    def is_full(self) -> bool:
        return self.current_nb_drone >= self.max_drone

    @model_validator(mode="after")
    def validate_rules(self) -> hub:
        if "-" in self.name:
            raise ValueError("'-' is not allowed in hub name!")
        if self.max_drone < 0:
            raise ValueError("Max drone must be a positive int!")
        try:
            if self.color != "none":
                Color(self.color)
        except ValueError:
            raise ValueError(f"{self.color} is not a valid color!")

        return self
