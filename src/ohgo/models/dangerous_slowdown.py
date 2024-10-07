from typing import Any, List

from .base_model import BaseModel
from .models import from_list, from_str, from_float, from_int, Link, to_float, to_class


class DangerousSlowdown(BaseModel):
    """
    DangerousSlowdown is a class for storing dangerous slowdown information.

    Attributes:
    normal_mph: The normal speed limit in MPH.
    current_mph: The current speed limit in MPH.
    route_name: The name of the route where the slowdown is located.
    direction: The direction the slowdown is affecting.
    """

    normal_mph: float
    current_mph: float
    route_name: str
    direction: str

    def __init__(self, links: List['Link'], id: str, latitude: float, longitude: float, location: str, description: str, normal_mph: float, current_mph: float, route_name: str, direction: str) -> None:
        super().__init__(links, id, latitude, longitude, location, description)  # Call the parent class initializer
        self.normal_mph = normal_mph
        self.current_mph = current_mph
        self.route_name = route_name
        self.direction = direction

    @staticmethod
    def from_dict(obj: Any) -> 'DangerousSlowdown':
        base_model = BaseModel.from_base_dict(obj)  # Reuse the parent class method for base fields
        normal_mph = from_float(obj.get("normalMPH"))
        current_mph = from_float(obj.get("currentMPH"))
        route_name = from_str(obj.get("routeName"))
        direction = from_str(obj.get("direction"))
        return DangerousSlowdown(base_model.links, base_model.id, base_model.latitude, base_model.longitude, base_model.location, base_model.description, normal_mph, current_mph, route_name, direction)

    def to_dict(self) -> dict:
        result = self.base_to_dict()  # Get the base attributes
        result.update({
            "normalMPH": from_float(self.normal_mph),
            "currentMPH": from_float(self.current_mph),
            "routeName": from_str(self.route_name),
            "direction": from_str(self.direction)
        })
        return result
