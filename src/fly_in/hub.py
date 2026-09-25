from __future__ import annotations

from pydantic import BaseModel, model_validator


class hub(BaseModel):
    name: str
    position: list[int]

    zone_type: str
    color: str
    max_drone: int

    @model_validator(mode="after")
    def validate_rules(self) -> hub:
        if "-" in self.name:
            raise ValueError("'-' is not allowed in hub name!")
        if self.max_drone < 0:
            raise ValueError("Max drone must be a positive int!")

        return self
