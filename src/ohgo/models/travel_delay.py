from dataclasses import dataclass
from typing import Any, List

from .base_model import BaseModel
from .models import Link, from_list, from_str, from_float, to_float, to_class, from_int


@dataclass
class TravelDelay(BaseModel):
    """
    TravelDelay is a class for storing travel delay information.

    Attributes:
    direction: The direction of the travel delay.
    route_name: The name of the route where the travel delay is located.
    travel_time: The travel time of the route.
    delay_time: The delay time of the route.
    start_mile_marker: The starting mile marker of the route.
    end_mile_marker: The ending mile marker of the route.
    current_avg_speed: The current average speed of the route.
    normal_avg_speed: The normal average speed of the route.
    """

    direction: str
    route_name: str
    travel_time: float
    delay_time: float
    start_mile_marker: float
    end_mile_marker: float
    current_avg_speed: float
    normal_avg_speed: float

    def __init__(self, links: List[Link], id: str, latitude: float, longitude: float, location: str, description: str, direction: str, route_name: str, travel_time: float, delay_time: float, start_mile_marker: float, end_mile_marker: float, current_avg_speed: float, normal_avg_speed: float) -> None:
        super().__init__(links, id, latitude, longitude, location, description)  # Call the parent class initializer
        self.direction = direction
        self.route_name = route_name
        self.travel_time = travel_time
        self.delay_time = delay_time
        self.start_mile_marker = start_mile_marker
        self.end_mile_marker = end_mile_marker
        self.current_avg_speed = current_avg_speed
        self.normal_avg_speed = normal_avg_speed

    @staticmethod
    def from_dict(obj: Any) -> 'TravelDelay':
        base_model = BaseModel.from_base_dict(obj)  # Reuse BaseModel for shared fields
        direction = from_str(obj.get("direction"))
        route_name = from_str(obj.get("routeName"))
        travel_time = from_float(obj.get("travelTime"))
        delay_time = from_float(obj.get("delayTime"))
        start_mile_marker = from_float(obj.get("startMileMarker"))
        end_mile_marker = from_float(obj.get("endMileMarker"))
        current_avg_speed = from_float(obj.get("currentAvgSpeed"))
        normal_avg_speed = from_float(obj.get("normalAvgSpeed"))
        return TravelDelay(base_model.links, base_model.id, base_model.latitude, base_model.longitude, base_model.location, base_model.description, direction, route_name, travel_time, delay_time, start_mile_marker, end_mile_marker, current_avg_speed, normal_avg_speed)

    def to_dict(self) -> dict:
        result = self.base_to_dict()  # Get the base attributes
        result.update({
            "direction": from_str(self.direction),
            "routeName": from_str(self.route_name),
            "travelTime": to_float(self.travel_time),
            "delayTime": to_float(self.delay_time),
            "startMileMarker": to_float(self.start_mile_marker),
            "endMileMarker": to_float(self.end_mile_marker),
            "currentAvgSpeed": from_float(self.current_avg_speed),
            "normalAvgSpeed": from_float(self.normal_avg_speed)
        })
        return result
