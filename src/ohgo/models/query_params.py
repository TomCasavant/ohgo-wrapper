from .models import *
from typing import Tuple
from dataclasses import dataclass

from ohgo.types import *
import logging
from enum import Enum

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def to_enum(enum_str, enum_type) -> Union[str, Enum]:
    """
    Attempts to convert a string to an Enum. If the string is not a valid Enum, it returns the string.
    :param enum_str: The string to convert
    :param enum_type: The Enum type to convert to
    :return: An Enum or the original string
    """
    enum = enum_str
    try:
        enum = enum_type(enum_str)
    except ValueError:
        logger.warning(f"{enum_str} may not be valid {enum_type.__name__}.")
    return enum


@dataclass
class QueryParams:
    """
    QueryParams is a dataclass for storing query parameters to pass to the OHGO API.

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
        if isinstance(self.region, str):
            self.region = to_enum(self.region, Region)

        if (self.map_bounds_sw and not self.map_bounds_ne) or (self.map_bounds_ne and not self.map_bounds_sw):
            logger.warning(f"Both map-bounds-sw and map-bounds-nw should be set.")

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


@dataclass
class DigitalSignParams(QueryParams):
    """
        DigitalSignParams is a dataclass for storing query parameters to pass to the OHGO. Has all parameters of QueryParams plus sign-type.
    """

    sign_type: Union[str, SignType] = None

    def __post_init__(self) -> None:
        """
        Post-init method for DigitalSignParams. Validates the sign_type attribute.
        """
        super().__post_init__()
        if not isinstance(self.sign_type, SignType):
            self.sign_type = to_enum(self.sign_type, SignType)

    def to_dict(self) -> dict:
        """
        Converts the DigitalSignParams object to a dictionary
        :return: A dictionary of the DigitalSignParams object
        """
        ep_params = super().to_dict()
        if self.sign_type:
            if isinstance(self.sign_type, Enum):
                sign_type = self.sign_type.value
            else:
                sign_type = self.sign_type
            ep_params["sign-type"] = sign_type
        return ep_params

    def __repr__(self):
        return f"DigitalSignParams({self.to_dict()})"

@dataclass
class ConstructionParams(QueryParams):
    """
    ConstructionParams is a dataclass for storing query parameters to pass to the OHGO API. Has all parameters of
    QueryParams plus construction-specific parameters, include_future and future_only.

    Attributes:
    include_future: Whether to include future construction, defaults to None. Format: True or False
    future_only: Whether to only include future construction, defaults to None. Format: True or False

    """

    include_future: Optional[datetime] = None
    future_only: Optional[datetime] = None

    def __post_init__(self) -> None:
        """
        Post-init method for ConstructionParams. Validates the include_future and future_only attributes.
        """
        super().__post_init__()
        if self.include_future and not isinstance(self.include_future, datetime):
            logger.warning(f"include_future should be a datetime object to automatically convert to yyyy-mm-dd")

        if self.future_only and not isinstance(self.future_only, datetime):
            logger.warning(f"future_only should be a datetime object to automatically convert to yyyy-mm-dd")
    def to_dict(self) -> dict:
        """
        Converts the ConstructionParams object to a dictionary
        :return: A dictionary of the ConstructionParams object
        """
        ep_params = super().to_dict()
        if self.include_future:
            if isinstance(self.include_future, datetime):
                include_future = self.include_future.strftime("%Y-%m-%d")
            else:
                include_future = self.include_future
            ep_params["include-future"] = include_future
        if self.future_only:
            if isinstance(self.future_only, datetime):
                future_only = self.future_only.strftime("%Y-%m-%d")
            else:
                future_only = self.future_only
            ep_params["future-only"] = future_only
        return ep_params

    def __repr__(self):
        return f"ConstructionParams({self.to_dict()})"

@dataclass
class WeatherSensorSiteParams(QueryParams):
    """
    WeatherSensorSiteParams is a dataclass for storing query parameters to pass to the OHGO API. Has all parameters
    of QueryParams plus weather sensor site-specific parameter: hazards_only.
    """

    hazards_only: Optional[bool] = None

    def to_dict(self) -> dict:
        """
        Converts the WeatherSensorSiteParams object to a dictionary
        :return: A dictionary of the WeatherSensorSiteParams object
        """
        ep_params = super().to_dict()
        if self.hazards_only:
            ep_params["hazards-only"] = self.hazards_only
        return ep_params

    def __repr__(self):
        return f"WeatherSensorSiteParams({self.to_dict()})"
