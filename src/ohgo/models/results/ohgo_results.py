from typing import TypeVar, List, Generic, Optional

from ohgo.models import Camera, DigitalSign, Construction, TravelDelay, DangerousSlowdown, WeatherSensorSite, Incident

T = TypeVar("T")


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
