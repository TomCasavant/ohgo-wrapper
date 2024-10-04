import logging
from ohgo_api.rest_adapter import RestAdapter
from ohgo_api.exceptions import OHGoException
from ohgo_api.models import *
from ohgo_api.image_fetcher import ImageFetcher
from typing import Any, List, TypeVar, Callable, Type, cast, Tuple
import json
from functools import singledispatchmethod
from enum import Enum
from dataclasses import dataclass

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class Region(Enum):
    AKRON = "akron"
    CINCINNATI = "cincinnati"
    CLEVELAND = "cleveland"
    COLUMBUS = "columbus"
    DAYTON = "dayton"
    TOLEDO = "toledo"
    CENTRAL_OHIO = "central-ohio"
    NE_OHIO = "ne-ohio"
    NW_OHIO = "nw-ohio"
    SE_OHIO = "se-ohio"
    SW_OHIO = "sw-ohio"
        
@dataclass
class QueryParams:
    region: Union[str, Region] = None
    map_bounds_sw: Optional[Tuple[float, float]] = None
    map_bounds_ne: Optional[tuple] = None
    page_size: Optional[int] = None
    page: Optional[int] = None
    page_all: Optional[bool] = None
    radius: Optional[Tuple[float, float, float]] = None

    def __post_init__(self):
        if not isinstance(self.region, Region):
            self.region = self.to_region(self.region)

        if (self.map_bounds_sw and not self.map_bounds_ne) or (self.map_bounds_ne and not self.map_bounds_sw):
            logger.warning(f"Both map-bounds-sw and map-bounds-nw should be set.")


    def to_region(self, region_str):
        region = region_str
        try:
            region = Region(region_str)
        except ValueError:
            logger.warning(f"{self.region} may not be valid Region." )
        return region

    def to_dict(self):
        ep_params = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Enum):
                    value = value.value
                elif isinstance(value, tuple):
                    value = ','.join(map(str, value))
                param_name = key.replace("_", "-") # OHGO API uses '-' in query vars
                ep_params[param_name] = value
        return ep_params

    def __iter__(self):
        return iter(self.to_dict().items())

    def __getitem__(self, key):
        return self.to_dict()[key]

    def __repr__(self):
        return f"QueryParams({self.to_dict()})"
                    
class OHGoClient:

    def __init__(
        self,
        hostname: str = "publicapi.ohgo.com",
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self._rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)
        self._image_fetcher = ImageFetcher(self._rest_adapter)

    def get_cameras(self, fetch_all=False, params: QueryParams=None, **kwargs) -> Camera:
        ep_params = dict(params) if params else {}
        ep_params.update(kwargs) # Add any extra arguments to ep_params
        
        result = self._rest_adapter.get(endpoint="cameras", fetch_all=fetch_all, ep_params=ep_params)
        cameras = [Camera.from_dict(camera) for camera in result.data]
        return cameras

    def get_camera(self, camera_id) -> Camera:
        result = self._rest_adapter.get(endpoint=f"cameras/{camera_id}")
        return Camera.from_dict(result.data[0])

    @singledispatchmethod
    def get_image(self, obj, size="small"):
        raise NotImplementedError("Cannot get image from this type")

    @get_image.register
    def _(self, camera_view: CameraView, size="small") -> Image.Image:
        if size == "small":
            return self._image_fetcher.fetch(camera_view.small_url)
        elif size == "large":
            return self._image_fetcher.fetch(camera_view.large_url)

    @get_image.register
    def _(self, camera: Camera, size="small") -> Image.Image:
        return self.get_image(camera.camera_views[0], size)

    def get_images(self, camera: Camera, size="small") -> List[Image.Image]:
        return [self.get_image(view) for view in camera.camera_views]
