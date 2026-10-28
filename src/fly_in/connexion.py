from __future__ import annotations

from .hub import Hub
from pydantic import model_validator, BaseModel, ValidationError


class Connexion(BaseModel):
    a: Hub
    b: Hub
    max_link_capacity: int = 1

    @model_validator(mode="after")
    def validate_rules(self) -> Connexion:
        if self.max_link_capacity < 0:
            raise ValidationError("max_link_capacity must be a positive int")
        return self
