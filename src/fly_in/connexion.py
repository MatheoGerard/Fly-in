"""
Connection model linking two hubs of a map.
"""

from __future__ import annotations

from .hub import Hub
from pydantic import model_validator, BaseModel, ValidationError


class Connexion(BaseModel):
    """
    Link between two hubs.

    Attributes:
        a: First hub of the link.
        b: Second hub of the link.
        max_link_capacity: Maximum number of drones allowed on the link at the
            same time.
    """

    a: Hub
    b: Hub
    max_link_capacity: int = 1

    @model_validator(mode="after")
    def validate_rules(self) -> Connexion:
        """
        Validate the connection once the model is created.

        Returns:
            The validated connection.

        Raises:
            ValidationError: If ``max_link_capacity`` is negative.
        """
        if self.max_link_capacity < 0:
            raise ValidationError("max_link_capacity must be a positive int")
        return self
