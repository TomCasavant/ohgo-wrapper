from typing import List, Dict, Any
from typing import *
from PIL import Image
from io import BytesIO
import requests

T = TypeVar("T")


class Result:

    _next_page: str = None
    
    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.links = data['links']
        self.total_result_count = data['totalResultCount']
        self.data = data['results'] if data else []
        self.rejected_filters = data['rejectedFilters']
        
    @property
    def next_page(self):
        if not self._next_page:
            for link in self.links:
                if link['rel'] == 'next-page':
                    self._next_page = link['href']
        return self._next_page


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


class CameraView:
    direction: str
    small_url: str
    large_url: str
    main_route: str

    def __init__(self, direction, small_url, large_url, main_route):
        self.direction = direction
        self.small_url = small_url
        self.large_url = large_url
        self.main_route = main_route
        self._small_image_cache = None
        self._large_image_cache = None

    @staticmethod
    def from_dict(obj: Any) -> "CameraView":
        assert isinstance(obj, dict)
        direction = from_str(obj.get("direction"))
        small_url = from_str(obj.get("smallUrl"))
        large_url = from_str(obj.get("largeUrl"))
        main_route = from_str(obj.get("mainRoute"))
        return CameraView(direction, small_url, large_url, main_route)

    def to_dict(self) -> dict:
        result: dict = {}
        result["direction"] = from_str(self.direction)
        result["smallUrl"] = from_str(self.small_url)
        result["largeUrl"] = from_str(self.large_url)
        result["mainRoute"] = from_str(self.main_route)
        return result

class Link:
    href: str
    rel: str

    def __init__(self, href="", rel=""):
        self.href = href
        self.rel = rel

    @staticmethod
    def from_dict(obj: Any) -> "Link":
        assert isinstance(obj, dict)
        href = from_str(obj.get("href"))
        rel = from_str(obj.get("rel"))
        return Link(href, rel)

    def to_dict(self) -> dict:
        result: dict = {}
        result["href"] = from_str(self.href)
        result["rel"] = from_str(self.rel)
        return result


class Camera:
    links: List[Link]
    id: str
    latitude: float
    longitude: float
    location: str
    description: str
    camera_views: List[CameraView]

    def __init__(
        self,
        links=None,
        id=None,
        latitude=None,
        longitude=None,
        location=None,
        description=None,
        camera_views=None,
        **kwargs
    ):
        self.id = id
        self.links = links
        self.latitude = latitude
        self.longitude = longitude
        self.location = location
        self.description = description
        self.camera_views = camera_views

    @staticmethod
    def from_dict(obj: Any) -> "Camera":
        assert isinstance(obj, dict)
        links = from_list(Link.from_dict, obj.get("links"))
        id = from_str(obj.get("id"))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        location = from_str(obj.get("location"))
        description = from_str(obj.get("description"))
        camera_views = from_list(CameraView.from_dict, obj.get("cameraViews"))
        return Camera(
            links, id, latitude, longitude, location, description, camera_views
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["links"] = from_list(lambda x: to_class(Link, x), self.links)
        result["id"] = from_str(self.id)
        result["latitude"] = to_float(self.latitude)
        result["longitude"] = to_float(self.longitude)
        result["location"] = from_str(self.location)
        result["description"] = from_str(self.description)
        result["cameraViews"] = from_list(
            lambda x: to_class(CameraView, x), self.camera_views
        )
        return result
