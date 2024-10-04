from typing import List

from ohgo_api.models.models import from_list, from_str, from_float, to_class, to_float, Link


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


class Camera:
    """
    Camera is a class for storing camera objects.

    Attributes:
    links: The links associated with the camera
    id: The ID of the camera
    latitude: The latitude of the camera
    longitude: The longitude of the camera
    location: The location of the camera
    description: The description of the camera. Usually relating to the camera's location
    camera_views: The views of the camera. Each view is a CameraView object that contains information about an image.

    Methods:
    from_dict: Converts a dictionary to a Camera object
    to_dict: Converts the Camera object to a dictionary

    """
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
        """
        Initializes the Camera object with the links, id, latitude, longitude, location, description, and camera views.
        :param links: A list of Link objects that relate to the Camera. Usually just a direct link to the camera's page.
        :param id: The ID of the camera
        :param latitude: The latitude of the camera's location
        :param longitude: The longitude of the camera's location
        :param location: The location of the camera. Usually a road or intersection.
        :param description: The description of the camera. Usually a description of the camera's location.
        :param camera_views: A list of CameraView objects that contain information about the camera's views.
        """
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
        result: dict = {"links": from_list(lambda x: to_class(Link, x), self.links), "id": from_str(self.id),
                        "latitude": to_float(self.latitude), "longitude": to_float(self.longitude),
                        "location": from_str(self.location), "description": from_str(self.description),
                        "cameraViews": from_list(
                            lambda x: to_class(CameraView, x), self.camera_views
                        )}
        return result
