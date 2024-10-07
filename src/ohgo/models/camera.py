from dataclasses import dataclass
from typing import List, Any

from .base_model import BaseModel
from .models import from_list, from_str, from_float, to_class, to_float, Link


@dataclass
class CameraView:
    """
    CameraView is a class for storing the view of a camera.

    Attributes:
    direction: The direction the camera is facing
    small_url: The URL of the small image
    large_url: The URL of the large image
    main_route: The main route of the camera

    Methods:
    from_dict: Converts a dictionary to a CameraView object
    to_dict: Converts the CameraView object to a dictionary
    """
    direction: str
    small_url: str
    large_url: str
    main_route: str

    def __init__(self, direction, small_url, large_url, main_route):
        """
        Initializes the CameraView object with the direction, small URL, large URL, and main route.
        :param direction: The direction the camera is facing as a string, PTZ if the camera is not in a fixed position
        :param small_url: URL link to the small image. Image snapshots are updated every 5 seconds.
        :param large_url: URL link to the large image. Image snapshots are updated every 5 seconds.
        :param main_route: The main road/intersection the camera is monitoring
        """
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
        result: dict = {"direction": from_str(self.direction), "smallUrl": from_str(self.small_url),
                        "largeUrl": from_str(self.large_url), "mainRoute": from_str(self.main_route)}
        return result

@dataclass
class Camera(BaseModel):
    """
    Camera is a class for storing camera objects.

    Attributes:
    camera_views: The views of the camera. Each view is a CameraView object that contains information about an image.

    """

    camera_views: List[CameraView]
    def __init__(
            self,
            links: List[Link],
            id: str,
            latitude: float,
            longitude: float,
            location: str,
            description: str,
            camera_views: List[CameraView]
    ):
        """
        Initializes the Camera object with common fields and camera views.
        :param links: A list of Link objects that relate to the Camera. Usually just a direct link to the camera's page.
        :param id: The ID of the camera.
        :param latitude: The latitude of the camera's location.
        :param longitude: The longitude of the camera's location.
        :param location: The location of the camera. Usually a road or intersection.
        :param description: The description of the camera's location.
        :param camera_views: A list of CameraView objects that contain information about the camera's views.
        """
        super().__init__(links, id, latitude, longitude, location, description)  # Call BaseModel's init
        self.camera_views = camera_views

    @staticmethod
    def from_dict(obj: Any) -> "Camera":
        """
        Converts a dictionary into a Camera object.
        :param obj: A dictionary representing a Camera object.
        :return: A Camera object.
        """
        base_model = BaseModel.from_base_dict(obj)  # Get common fields using BaseModel
        camera_views = from_list(CameraView.from_dict, obj.get("cameraViews"))
        return Camera(base_model.links, base_model.id, base_model.latitude, base_model.longitude, base_model.location, base_model.description, camera_views)

    def to_dict(self) -> dict:
        """
        Converts the Camera object into a dictionary.
        :return: A dictionary representation of the Camera object.
        """
        result = self.base_to_dict()  # Get common fields from BaseModel
        result.update({
            "cameraViews": from_list(lambda x: to_class(CameraView, x), self.camera_views)
        })
        return result
