from dataclasses import dataclass
from typing import List, Any

from .models import from_list, from_str, from_float, Link, to_class, to_float

@dataclass
class BaseModel:

    links: List[Link]
    id: str
    latitude: float
    longitude: float
    location: str
    description: str

    def __init__(self, links: List['Link'], id: str, latitude: float, longitude: float, location: str, description: str) -> None:
        self.links = links
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.location = location
        self.description = description

    @staticmethod
    def from_base_dict(obj: Any) -> 'BaseModel':
        assert isinstance(obj, dict)
        links = from_list(Link.from_dict, obj.get("links"))
        id = from_str(obj.get("id"))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        location = from_str(obj.get("location"))
        description = from_str(obj.get("description"))
        return BaseModel(links, id, latitude, longitude, location, description)

    def base_to_dict(self) -> dict:
        result: dict = {
            "links": from_list(lambda x: to_class(Link, x), self.links),
            "id": from_str(self.id),
            "latitude": to_float(self.latitude),
            "longitude": to_float(self.longitude),
            "location": from_str(self.location),
            "description": from_str(self.description)
        }
        return result
