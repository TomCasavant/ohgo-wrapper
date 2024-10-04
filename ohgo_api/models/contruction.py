from dataclasses import dataclass
from datetime import datetime
from typing import List, Any

from ohgo_api.models.models import Link, from_list, from_str, from_float, from_datetime, to_float, to_class


@dataclass
class Construction:
    links: List[Link]
    id: str
    latitude: float
    longitude: float
    location: str
    description: str
    category: str
    direction: str
    district: None
    route_name: str
    status: str
    start_date: datetime
    end_date: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'Construction':
        assert isinstance(obj, dict)
        links = from_list(Link.from_dict, obj.get("links"))
        id = from_str(obj.get("id"))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        location = from_str(obj.get("location"))
        description = from_str(obj.get("description"))
        category = from_str(obj.get("category"))
        direction = from_str(obj.get("direction"))
        district = from_str(obj.get("district"))
        route_name = from_str(obj.get("routeName"))
        status = from_str(obj.get("status"))
        start_date = from_datetime(obj.get("startDate"))
        end_date = from_datetime(obj.get("endDate"))
        return Construction(links, id, latitude, longitude, location, description, category, direction, district,
                            route_name, status, start_date, end_date)

    def to_dict(self) -> dict:
        result: dict = {"links": from_list(lambda x: to_class(Link, x), self.links), "id": from_str(self.id),
                        "latitude": to_float(self.latitude), "longitude": to_float(self.longitude),
                        "location": from_str(self.location), "description": from_str(self.description),
                        "category": from_str(self.category), "direction": from_str(self.direction),
                        "district": from_str(self.district), "routeName": from_str(self.route_name),
                        "status": from_str(self.status), "startDate": self.start_date.isoformat(),
                        "endDate": self.end_date.isoformat()}
        return result
