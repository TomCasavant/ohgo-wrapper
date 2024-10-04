from ohgo_api.models.models import *
from typing import Tuple
from enum import Enum
from dataclasses import dataclass

from ohgo_api.models.region import Region
from ohgo_api.ohgo_client import logger


@dataclass
class QueryParams:
    """
    QueryParams is a dataclass for storing query parameters to pass to the OHGo API.

    Attributes:
    region: The region to query, defaults to None. Format: Region enum or string
    map_bounds_sw: The southwest corner of a bounding box, defaults to None. Format: (lat, lon)
    map_bounds_ne: The northeast corner of a bounding box, defaults to None. Format: (lat, lon)
    page_size: The number of results to return per page, defaults to None. Format: int
    page: The page number to return, defaults to None. Format: int
    page_all: Whether to fetch all pages, defaults to None. Format: True or False
    radius: The radius to search around a point, defaults to None. Format: (lat, lon, radius)

    Methods:
    to_region: Converts a string to a Region enum
    to_dict: Converts the QueryParams object to a dictionary
    """

    region: Union[str, Region] = None
    map_bounds_sw: Optional[Tuple[float, float]] = None
    map_bounds_ne: Optional[tuple] = None
    page_size: Optional[int] = None
    page: Optional[int] = None
    page_all: Optional[bool] = None
    radius: Optional[Tuple[float, float, float]] = None

    def __post_init__(self) -> None:
        """
        Post-init method for QueryParams. Validates the region attribute.
        """
        if not isinstance(self.region, Region):
            self.region = self.to_region(self.region)

        if (self.map_bounds_sw and not self.map_bounds_ne) or (self.map_bounds_ne and not self.map_bounds_sw):
            logger.warning(f"Both map-bounds-sw and map-bounds-nw should be set.")

    def to_region(self, region_str) -> Union[str, Region]:
        """
        Attempts to convert a string to a Region enum. If the string is not a valid Region, it returns the string.
        :param region_str: The string to convert
        :return: A Region enum or the original string
        """
        region = region_str
        try:
            region = Region(region_str)
        except ValueError:
            logger.warning(f"{self.region} may not be valid Region.")
        return region

    def to_dict(self) -> dict:
        """
        Converts the QueryParams object to a dictionary
        :return: A dictionary of the QueryParams object
        """
        ep_params = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Enum):
                    value = value.value
                elif isinstance(value, tuple):
                    value = ','.join(map(str, value))
                param_name = key.replace("_", "-")  # OHGO API uses '-' in query vars
                ep_params[param_name] = value
        return ep_params

    def __iter__(self):
        return iter(self.to_dict().items())

    def __getitem__(self, key):
        return self.to_dict()[key]

    def __repr__(self):
        return f"QueryParams({self.to_dict()})"
