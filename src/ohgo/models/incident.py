from dataclasses import dataclass
from typing import Any, List

from .base_model import BaseModel
from .models import Link, from_list, from_str, from_float, to_float, to_class

@dataclass
class Incident(BaseModel):
    """
    Incident is a class for storing incident information.

    Attributes:
    category: The category of the incident.
    direction: The direction related to the incident.
    route_name: The name of the route where the incident is located.
    road_status: The current status of the road.
    """

    category: str
    direction: str
    route_name: str
    road_status: str

    def __init__(self, links: List['Link'], id: str, latitude: float, longitude: float, location: str, description: str, category: str, direction: str, route_name: str, road_status: str) -> None:
        super().__init__(links, id, latitude, longitude, location, description)  # Call the parent class initializer
        self.category = category
        self.direction = direction
        self.route_name = route_name
        self.road_status = road_status

    @staticmethod
    def from_dict(obj: Any) -> 'Incident':
        base_model = BaseModel.from_base_dict(obj)  # Reuse BaseModel for shared fields
        category = from_str(obj.get("category"))
        direction = from_str(obj.get("direction"))
        route_name = from_str(obj.get("routeName"))
        road_status = from_str(obj.get("roadStatus"))
        return Incident(base_model.links, base_model.id, base_model.latitude, base_model.longitude, base_model.location, base_model.description, category, direction, route_name, road_status)

    def to_dict(self) -> dict:
        result = self.base_to_dict()  # Get the base attributes
        result.update({
            "category": from_str(self.category),
            "direction": from_str(self.direction),
            "routeName": from_str(self.route_name),
            "roadStatus": from_str(self.road_status)
        })
        return result
