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

    def get_color(self) -> Color | str:
        if self.color == "none" or self.color == "rainbow":
            return Color("aqua")

        return Color(self.color)

    def get_true_x(self, sub_value, offset_x) -> int:
        return (self.position[0] - sub_value + 1) * offset_x

    def get_true_y(self, sub_value, offset_y) -> int:
        return (self.position[1] - sub_value + 1) * offset_y

    @model_validator(mode="after")
    def validate_rules(self) -> hub:
        if "-" in self.name:
            raise ValueError("'-' is not allowed in hub name!")
        if self.max_drone < 0:
            raise ValueError("Max drone must be a positive int!")

        return self
