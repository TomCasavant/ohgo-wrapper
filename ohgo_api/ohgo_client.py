import logging

from PIL.Image import Image

from ohgo_api.models.camera import Camera, CameraView
from ohgo_api.models.query_params import QueryParams
from ohgo_api.rest_adapter import RestAdapter
from ohgo_api.exceptions import OHGoException
from ohgo_api.image_handler import ImageHandler
from typing import List
from functools import singledispatchmethod

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class OHGoClient:
    """
    OHGoClient provides methods for fetching data from OHGo including Cameras, Construction, Digital Signage,
    Incidents, Travel Delays, and Weather Sensors.

    Attributes:
    _rest_adapter: RestAdapter for making HTTP requests to the OHGo API
    _image_handler: ImageHandler for fetching images from OHGo API

    Methods:
    get_cameras: Fetches cameras from OHGo API
    get_camera: Fetches a single camera from OHGo API
    get_image: Fetches an image from a Camera or CameraView
    get_images: Fetches images from all CameraViews of a Camera

    """

    def __init__(
            self,
            api_key: str,
            hostname: str = "publicapi.ohgo.com",
            ver: str = "v1",
            ssl_verify: bool = True,
            logger: logging.Logger = None,
    ):
        """
        Constructor for OHGoClient
        :param api_key: Required API key for OHGo API
        :param hostname: The hostname of the OHGo API, almost always "publicapi.ohgo.com"
        :param ver: The version of the API to use, defaults to "v1"
        :param ssl_verify: Whether to verify SSL certificates, defaults to True
        :param logger: (optional) A logger to use for logging, defaults to None
        """
        self._rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)
        self._image_handler = ImageHandler(self._rest_adapter)

    def get_cameras(self, params: QueryParams = None, fetch_all=False, **kwargs) -> List[Camera]:
        """
        Fetches cameras from the OHGo API
        :param params: QueryParams object to pass to the API
        :param fetch_all: Pages through all results if True. Recommended to use page-all param instead.
        :param kwargs: Extra arguments to pass to the API. QueryParams recommended instead. (provides basic validation)
        :return: List of Camera objects
        """
        ep_params = dict(params) if params else {}
        ep_params.update(kwargs)  # Add any extra arguments to ep_params

        result = self._rest_adapter.get(endpoint="cameras", fetch_all=fetch_all, ep_params=ep_params)
        cameras = [Camera.from_dict(camera) for camera in result.data]
        return cameras

    def get_camera(self, camera_id) -> Camera:
        """
        Fetches a single camera from the OHGo API
        :param camera_id: The ID of the camera to fetch
        :return: A Camera object
        """
        result = self._rest_adapter.get(endpoint=f"cameras/{camera_id}")
        if len(result.data) == 0:
            raise OHGoException(f"No camera found with ID {camera_id}")
        return Camera.from_dict(result.data[0])

    @singledispatchmethod
    def get_image(self, obj, size="small"):
        """
        Generic method for fetching an image from an object. Not implemented for all types.
        :param obj: The object to fetch the image from
        :param size: the size of the image to fetch, either "small" or "large"
        :return: A PIL Image object
        """
        raise NotImplementedError("Cannot get image from this type")

    @get_image.register
    def _(self, camera_view: CameraView, size="small") -> Image:
        """
        Fetches an image from a CameraView
        :param camera_view: A CameraView object.
        :param size: the size of the image to fetch, either "small" or "large"
        :return: A PIL Image object
        """
        if size == "small":
            return self._image_handler.fetch(camera_view.small_url)
        elif size == "large":
            return self._image_handler.fetch(camera_view.large_url)

    @get_image.register
    def _(self, camera: Camera, size="small") -> Image:
        """
        Fetches an image from a Camera
        :param camera: A Camera object
        :param size: the size of the image to fetch, either "small" or "large"
        :return: The first CameraView image as a PIL Image object
        """
        if len(camera.camera_views) == 0:
            raise OHGoException(f"No camera views found for camera {camera.id}")
        return self.get_image(camera.camera_views[0], size)

    def get_images(self, camera: Camera, size="small") -> List[Image]:
        """
        Loops through all CameraViews of a Camera and fetches images for each.
        :param camera: A Camera object
        :param size: the size of the image to fetch, either "small" or "large"
        :return: List of PIL Image objects
        """
        return [self.get_image(view, size) for view in camera.camera_views]
