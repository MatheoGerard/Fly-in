"""
Hub model: a zone of the map where drones can stay.
"""

from __future__ import annotations

from pygame import Color
from pydantic import BaseModel, model_validator


class Hub(BaseModel):
    """
    Zone of the map where drones can stay.

    Attributes:
        name: Name of the hub (must not contain '-').
        position: Coordinates ``[x, y]`` of the hub on the map.
        zone_type: Type of zone: ``normal``, ``blocked``, ``restricted`` or
            ``priority``.
        color: Name of a pygame color, ``none`` or ``rainbow``.
        max_drone: Maximum number of drones the hub can hold.
        state: Role of the hub: 0 for start, 1 for a regular hub, 2 for end.
        neighbor: Hubs directly connected to this one.
        cost: Cost of moving to this hub.
        current_nb_drone: Number of drones currently in the hub.
        visited: Whether the hub has been visited.
    """

    name: str
    position: list[int]

    zone_type: str
    color: str
    max_drone: int
    state: int

    neighbor: list[Hub] = []
    cost: float = 0
    current_nb_drone: int = 0
    visited: bool = False

    def define_cost(self) -> None:
        """
        Set the movement cost of the hub from its zone type.

        A blocked zone costs infinity, a restricted zone 2.0, a priority zone
        0.999999 and any other zone 1.0.
        """
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
        """
        Get the color used to draw the hub.

        Returns:
            Aqua if the color is ``none`` or ``rainbow``, otherwise the pygame
            color matching the color name.
        """
        if self.color == "none" or self.color == "rainbow":
            return Color("aqua")

        return Color(self.color)

    def get_true_x(self, sub_value: int, offset_x: int) -> int:
        """
        Convert the x coordinate of the hub to a screen position.

        Args:
            sub_value: Smallest x coordinate among all the hubs, used to shift
                the map towards the origin.
            offset_x: Horizontal spacing in pixels between two coordinates.

        Returns:
            The x position of the hub on screen, in pixels.
        """
        return (self.position[0] - sub_value + 1) * offset_x

    def get_true_y(self, sub_value: int, offset_y: int) -> int:
        """
        Convert the y coordinate of the hub to a screen position.

        Args:
            sub_value: Smallest y coordinate among all the hubs, used to shift
                the map towards the origin.
            offset_y: Vertical spacing in pixels between two coordinates.

        Returns:
            The y position of the hub on screen, in pixels.
        """
        return (self.position[1] - sub_value + 1) * offset_y

    def update_current_nb_drone(self, change_value: int) -> None:
        """
        Change the number of drones currently in the hub.

        Args:
            change_value: Value added to the counter (negative to remove
                drones).
        """
        self.current_nb_drone += change_value

    def is_full(self) -> bool:
        """
        Check whether the hub reached its capacity.

        Returns:
            True if the number of drones is greater than or equal to
            ``max_drone``, False otherwise.
        """
        return self.current_nb_drone >= self.max_drone

    @model_validator(mode="after")
    def validate_rules(self) -> Hub:
        """
        Validate the hub once the model is created.

        Returns:
            The validated hub.

        Raises:
            ValueError: If the name contains '-', if ``max_drone`` is negative,
                if the zone type is not valid or if the color is not a valid
                pygame color.
        """
        if "-" in self.name:
            raise ValueError("'-' is not allowed in hub name!")
        if self.max_drone < 0:
            raise ValueError("Max drone must be a positive int!")
        if (
            self.zone_type != "blocked"
            and self.zone_type != "restricted"
            and self.zone_type != "normal"
            and self.zone_type != "priority"
        ):
            raise ValueError(f"{self.zone_type} is not a zone type valid!")
        try:
            if self.color != "none" and self.color != "rainbow":
                Color(self.color)
        except ValueError:
            raise ValueError(f"{self.color} is not a valid color!")

        return self
