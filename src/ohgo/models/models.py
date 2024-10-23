from dataclasses import dataclass
from datetime import datetime
from typing import *

import dateutil.parser

from . import Camera, Incident, DigitalSign, Construction, TravelDelay, DangerousSlowdown, \
    WeatherSensorSite

T = TypeVar("T")


class Result:
    """
    Result is a class for storing the results of an OHGO API query.

    Attributes:
    status_code: The status code of the query as an integer
    message: The message returned from the query
    links: The links returned from the query
    total_result_count: The total number of results returned from the query
    data: The results returned from the query. Each result is a dictionary. Default is an empty list
    rejected_filters: The rejected filters returned from the query. Default is an empty list
    _next_page: The next page of results

    Methods:
    next_page: Returns the next page of results
    """

    _next_page: str = None

    def __init__(self, status_code: int, message: str = "", data: Dict = None):
        """
        Initializes the Result object with the status code, message, and data.
        :param status_code: The response status code
        :param message: The response message
        :param data: The response data
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.links = data['links']
        self.total_result_count = data['totalResultCount']
        self.data = data['results'] if data else []
        self.rejected_filters = data['rejectedFilters']

    @property
    def next_page(self):
        """
        Returns the next page of results
        :return: If there is a next page, returns the URL of the next page. Otherwise, returns None
        """
        if not self._next_page:
            for link in self.links:
                if link['rel'] == 'next-page':
                    self._next_page = link['href']
        return self._next_page


@dataclass
class CachedResult:
    status_code: int = 304
    message: str = "Data has not changed since the last request"
    etag: str = None


class OHGOListResult(Generic[T]):
    """
    OHGOListResult is a class for storing a list of items. It behaves like a list
    while still allowing access to an etag, if applicable.
    """

    def __init__(self, items: List[T], etag: str = None, cached: bool = False):
        self.items = items
        self.etag = etag
        self.cached = cached

    def __getattr__(self, attr):
        # Delegate attribute access to the internal list if not found in OHGOListResult
        return getattr(self.items, attr)

    def __getitem__(self, index):
        # Allow index-based access to items (e.g., result[0])
        return self.items[index]

    def __iter__(self):
        # Make the result iterable (e.g., for item in result)
        return iter(self.items)

    def __len__(self):
        # Return the length of the items list
        return len(self.items)

    def __repr__(self):
        return f"{type(self.items).__name__}ListResult({self.items}, etag={self.etag})"

    def __call__(self):
        # Allow the result object to return the items list when called
        return self.items


class OHGOItemResult(Generic[T]):
    """
    OHGOItemResult is a class for storing an individual item. The result behaves as the item itself,
    while still allowing access to its etag attribute.
    """

    def __init__(self, item: T, etag: str = None, cached: bool = False):
        self.item = item
        self.etag = etag
        self.cached = cached

    def __getattr__(self, attr):
        # If the attribute doesn't exist on OHGOItemResult, delegate to the item.
        return getattr(self.item, attr)

    def __repr__(self):
        return f"{type(self.item).__name__}ItemResult({self.item}, etag={self.etag})"

    def __call__(self):
        # Allow the object to behave like the item when called
        return self.item

    def __iter__(self):
        # If you want to treat the result as the item when used in iterations
        yield self.item

    def __getitem__(self, key):
        # Access the item like an indexable object (e.g., result[0])
        if key == 0:
            return self.item
        raise IndexError("OHGOItemResult only contains one item.")


class CameraListResult(OHGOListResult[Optional[Camera]]):
    pass


class CameraItemResult(OHGOItemResult[Optional[Camera]]):
    pass


class DigitalSignListResult(OHGOListResult[Optional[DigitalSign]]):
    pass


class DigitalSignItemResult(OHGOItemResult[Optional[DigitalSign]]):
    pass


class ConstructionListResult(OHGOListResult[Optional[Construction]]):
    pass


class ConstructionItemResult(OHGOItemResult[Optional[Construction]]):
    pass


class TravelDelayListResult(OHGOListResult[Optional[TravelDelay]]):
    pass


class TravelDelayItemResult(OHGOItemResult[Optional[TravelDelay]]):
    pass


class DangerousSlowdownListResult(OHGOListResult[Optional[DangerousSlowdown]]):
    pass


class DangerousSlowdownItemResult(OHGOItemResult[Optional[DangerousSlowdown]]):
    pass


class WeatherSensorSiteListResult(OHGOListResult[Optional[WeatherSensorSite]]):
    pass


class WeatherSensorSiteItemResult(OHGOItemResult[Optional[WeatherSensorSite]]):
    pass


class IncidentListResult(OHGOListResult[Optional[Incident]]):
    pass


class IncidentItemResult(OHGOItemResult[Optional[Incident]]):
    pass


def from_str(x: Any) -> str:
    if x is None:
        return ""
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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


class Link:
    """
    Link is a class for storing a link object.

    Attributes:
    href: The URL of the link
    rel: The relationship of the link to the object
    """
    href: str
    rel: str

    def __init__(self, href="", rel=""):
        """
        Initializes the Link object with the href and rel.
        :param href: The URL of the link
        :param rel: The relationship of the link to the object
        """
        self.href = href
        self.rel = rel

    @staticmethod
    def from_dict(obj: Any) -> "Link":
        assert isinstance(obj, dict)
        href = from_str(obj.get("href"))
        rel = from_str(obj.get("rel"))
        return Link(href, rel)

    def to_dict(self) -> dict:
        result: dict = {"href": from_str(self.href), "rel": from_str(self.rel)}
        return result
