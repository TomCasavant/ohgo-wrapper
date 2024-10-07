import logging

from PIL.Image import Image

from .models import Camera, CameraView, Construction, DigitalSign, Incident, TravelDelay, WeatherSensorSite, DangerousSlowdown
from .models import QueryParams, DigitalSignParams, ConstructionParams, WeatherSensorSiteParams

from ohgo.rest_adapter import RestAdapter
from ohgo.exceptions import OHGOException
from ohgo.image_handler import ImageHandler
from typing import List
from functools import singledispatchmethod

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class OHGOClient:
    """
    OHGOClient provides methods for fetching data from OHGO including Cameras, Construction, Digital Signage,
    Incidents, Travel Delays, and Weather Sensors.

    Attributes:
    _rest_adapter: RestAdapter for making HTTP requests to the OHGO API
    _image_handler: ImageHandler for fetching images from OHGO API

    Methods:
    get_cameras: Fetches cameras from OHGO API
    get_camera: Fetches a single camera from OHGO API
    get_image: Fetches an image from a Camera or CameraView
    get_images: Fetches images from all CameraViews of a Camera
    get_digital_signs: Fetches digital signs from OHGO API
    get_digital_sign: Fetches a single digital sign from OHGO API
    get_constructions: Fetches construction from OHGO API
    get_construction: Fetches a single construction from OHGO API
    get_weather_sensor_sites: Fetches weather sensor sites from OHGO API
    get_weather_sensor_site: Fetches a single weather sensor site from OHGO API
    get_incidents: Fetches incidents from OHGO API
    get_incident: Fetches a single incident from OHGO API
    get_dangerous_slowdowns: Fetches dangerous slowdowns from OHGO API
    get_dangerous_slowdown: Fetches a single dangerous slowdown from OHGO API

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
        Constructor for OHGOClient
        :param api_key: Required API key for OHGO API
        :param hostname: The hostname of the OHGO API, almost always "publicapi.ohgo.com"
        :param ver: The version of the API to use, defaults to "v1"
        :param ssl_verify: Whether to verify SSL certificates, defaults to True
        :param logger: (optional) A logger to use for logging, defaults to None
        """
        self._rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)
        self._image_handler = ImageHandler(self._rest_adapter)

    def get_cameras(self, params: QueryParams = None, fetch_all=False, **kwargs) -> List[Camera]:
        """
        Fetches cameras from the OHGO API
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
        Fetches a single camera from the OHGO API
        :param camera_id: The ID of the camera to fetch
        :return: A Camera object
        """
        result = self._rest_adapter.get(endpoint=f"cameras/{camera_id}")
        if len(result.data) == 0:
            raise OHGOException(f"No camera found with ID {camera_id}")
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
            raise OHGOException(f"No camera views found for camera {camera.id}")
        return self.get_image(camera.camera_views[0], size)

    @singledispatchmethod
    def get_images(self, obj) -> List[Image]:
        """
        Generic method for fetching images from an object. Not implemented for all types.
        :param obj: The object to fetch images from
        :return: List of PIL Image objects
        """
        raise NotImplementedError("Cannot get images from this type")

    @get_images.register
    def _(self, camera: Camera, size="small") -> List[Image]:
        """
        Loops through all CameraViews of a Camera and fetches images for each.
        :param camera: A Camera object
        :param size: the size of the image to fetch, either "small" or "large"
        :return: List of PIL Image objects
        """
        return [self.get_image(view, size) for view in camera.camera_views]

    @get_images.register
    def _(self, digital_sign: DigitalSign) -> List[Image]:
        """
        Fetches all images from a DigitalSign. Filters out any None values.
        :param digital_sign:
        :return: a list of PIL Image objects associated with the DigitalSign
        """
        # fetch might return None due to request exceptions, we don't want those values
        images = [self._image_handler.fetch(image_url) for image_url in digital_sign.image_urls]
        return [image for image in images if image is not None]

    def get_digital_signs(self, params: DigitalSignParams = None, fetch_all=False, **kwargs) -> List[DigitalSign]:
        """
        Fetches digital signs from the OHGO API
        :param params: DigitalSignParams object to pass to the API
        :param fetch_all: Pages through all results if True. Recommended to use page-all param instead.
        :param kwargs: Extra arguments to pass to the API.
        :return: List of DigitalSign objects
        """
        ep_params = dict(params) if params else {}
        ep_params.update(kwargs)

        result = self._rest_adapter.get(endpoint="digital-signs", fetch_all=fetch_all, ep_params=ep_params)
        digital_signs = [DigitalSign.from_dict(digital_sign) for digital_sign in result.data]
        return digital_signs

    def get_digital_sign(self, digital_sign_id) -> DigitalSign:
        """
        Fetches a single digital sign from the OHGO API
        :param digital_sign_id: The ID of the digital sign to fetch
        :return: A DigitalSign object
        """
        result = self._rest_adapter.get(endpoint=f"digital-signs/{digital_sign_id}")
        if len(result.data) == 0:
            raise OHGOException(f"No digital sign found with ID {digital_sign_id}")
        return DigitalSign.from_dict(result.data[0])

    def get_constructions(self, params: ConstructionParams = None, fetch_all=False, **kwargs) -> List[Construction]:
        """
        Fetches construction from the OHGO API
        :param params: ConstructionParams object to pass to the API
        :param fetch_all: Pages through all results if True. Recommended to use page-all param instead.
        :param kwargs: Extra arguments to pass to the API.
        :return: List of Construction objects
        """
        ep_params = dict(params) if params else {}
        ep_params.update(kwargs)

        result = self._rest_adapter.get(endpoint="construction", fetch_all=fetch_all, ep_params=ep_params)
        construction = [Construction.from_dict(construction) for construction in result.data]
        return construction

    def get_construction(self, construction_id) -> Construction:
        """
        Fetches a single construction from the OHGO API
        :param construction_id: The ID of the construction to fetch
        :return: A Construction object
        """
        result = self._rest_adapter.get(endpoint=f"construction/{construction_id}")
        if len(result.data) == 0:
            raise OHGOException(f"No construction found with ID {construction_id}")
        return Construction.from_dict(result.data[0])

    def get_weather_sensor_sites(self, params: WeatherSensorSiteParams = None, fetch_all=False, **kwargs) -> List[WeatherSensorSite]:
        """
        Fetches weather sensor sites from the OHGO API
        :param params: WeatherSensorSiteParams object to pass to the API
        :param fetch_all: Pages through all results if True. Recommended to use page-all param instead.
        :param kwargs: Extra arguments to pass to the API.
        :return: List of WeatherSensorSite objects
        """
        ep_params = dict(params) if params else {}
        ep_params.update(kwargs)

        result = self._rest_adapter.get(endpoint="weather-sensor-sites", fetch_all=fetch_all, ep_params=ep_params)
        weather_sensor_sites = [WeatherSensorSite.from_dict(weather_sensor_site) for weather_sensor_site in result.data]
        return weather_sensor_sites

    def get_weather_sensor_site(self, site_id) -> WeatherSensorSite:
        """
        Fetches a single weather sensor site from the OHGO API
        :param site_id: The ID of the weather sensor site to fetch
        :return: A WeatherSensorSite object
        """
        result = self._rest_adapter.get(endpoint=f"weather-sensor-sites/{site_id}")
        if len(result.data) == 0:
            raise OHGOException(f"No weather sensor site found with ID {site_id}")
        return WeatherSensorSite.from_dict(result.data[0])

    def get_incidents(self, params: QueryParams = None, fetch_all=False, **kwargs) -> List[Incident]:
        """
        Fetches incidents from the OHGO API
        :param params: QueryParams object to pass to the API
        :param fetch_all: Pages through all results if True. Recommended to use page-all param instead.
        :param kwargs: Extra arguments to pass to the API.
        :return: List of Incident objects
        """
        result = self._rest_adapter.get(endpoint="incidents", fetch_all=fetch_all, ep_params=dict(params) if params else kwargs)
        incidents = [Incident.from_dict(incident) for incident in result.data]
        return incidents

    def get_incident(self, incident_id) -> Incident:
        """
        Fetches a single incident from the OHGO API
        :param incident_id: The ID of the incident to fetch
        :return: An Incident object
        """
        result = self._rest_adapter.get(endpoint=f"incidents/{incident_id}")
        if len(result.data) == 0:
            raise OHGOException(f"No incident found with ID {incident_id}")
        return Incident.from_dict(result.data[0])

    def get_dangerous_slowdowns(self, params: QueryParams = None, fetch_all=False, **kwargs) -> List[DangerousSlowdown]:
        """
        Fetches dangerous slowdowns from the OHGO API
        :param params: QueryParams object to pass to the API
        :param fetch_all: Pages through all results if True. Recommended to use page-all param instead.
        :param kwargs: Extra arguments to pass to the API.
        :return: List of DangerousSlowdown objects
        """
        result = self._rest_adapter.get(endpoint="dangerous-slowdowns", fetch_all=fetch_all, ep_params=dict(params) if params else kwargs)
        slowdowns = [DangerousSlowdown.from_dict(slowdown) for slowdown in result.data]
        return slowdowns

    def get_dangerous_slowdown(self, slowdown_id) -> DangerousSlowdown:
        """
        Fetches a single dangerous slowdown from the OHGO API
        :param slowdown_id: The ID of the dangerous slowdown to fetch
        :return: A DangerousSlowdown object
        """
        result = self._rest_adapter.get(endpoint=f"dangerous-slowdowns/{slowdown_id}")
        if len(result.data) == 0:
            raise OHGOException(f"No dangerous slowdown found with ID {slowdown_id}")
        return DangerousSlowdown.from_dict(result.data[0])

    def get_travel_delays(self, params: QueryParams = None, fetch_all=False, **kwargs) -> List[TravelDelay]:
        """
        Fetches travel delays from the OHGO API
        :param params: QueryParams object to pass to the API
        :param fetch_all: Pages through all results if True. Recommended to use page-all param instead.
        :param kwargs: Extra arguments to pass to the API.
        :return: List of TravelDelay objects
        """
        result = self._rest_adapter.get(endpoint="travel-delays", fetch_all=fetch_all, ep_params=dict(params) if params else kwargs)
        delays = [TravelDelay.from_dict(delay) for delay in result.data]
        return delays

    def get_travel_delay(self, delay_id) -> TravelDelay:
        """
        Fetches a single travel delay from the OHGO API
        :param delay_id: The ID of the travel delay to fetch
        :return: A TravelDelay object
        """
        result = self._rest_adapter.get(endpoint=f"travel-delays/{delay_id}")
        if len(result.data) == 0:
            raise OHGOException(f"No travel delay found with ID {delay_id}")
