from dataclasses import dataclass
from typing import List, Any

from ohgo_api.models.models import from_list, from_str, from_float, to_float, to_class, Link


@dataclass
class DigitalSign:
    links: List[Link]
    id: int
    latitude: float
    longitude: float
    location: str
    description: str
    sign_type_name: str
    messages: List[str]
    image_urls: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> 'DigitalSign':
        assert isinstance(obj, dict)
        links = from_list(Link.from_dict, obj.get("links"))
        id = int(from_str(obj.get("id")))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        location = from_str(obj.get("location"))
        description = from_str(obj.get("description"))
        sign_type_name = from_str(obj.get("signTypeName"))
        messages = from_list(from_str, obj.get("messages"))
        image_urls = from_list(lambda x: x, obj.get("imageUrls"))
        return DigitalSign(links, id, latitude, longitude, location, description, sign_type_name, messages, image_urls)

    def to_dict(self) -> dict:
        result: dict = {"links": from_list(lambda x: to_class(Link, x), self.links), "id": from_str(str(self.id)),
                        "latitude": to_float(self.latitude), "longitude": to_float(self.longitude),
                        "location": from_str(self.location), "description": from_str(self.description),
                        "signTypeName": from_str(self.sign_type_name), "messages": from_list(from_str, self.messages),
                        "imageUrls": from_list(lambda x: x, self.image_urls)}
        return result
