from dataclasses import dataclass
from datetime import datetime
from typing import List, Any, Optional

from .base_model import BaseModel
from .models import from_list, from_str, Link, from_float, to_class, to_float, from_bool, \
    from_datetime, from_int


@dataclass
class AtmosphericSensor:
    air_temperature: float
    dewpoint_temperature: float
    humidity: float
    average_wind_speed: float
    maximum_wind_speed: float
    wind_direction: str
    precipitation: str
    precipitation_rate: float
    visibility: float
    last_update: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'AtmosphericSensor':
        assert isinstance(obj, dict)
        air_temperature = from_float(obj.get("airTemperature"))
        dewpoint_temperature = from_float(obj.get("dewpointTemperature"))
        humidity = from_float(obj.get("humidity"))
        average_wind_speed = from_float(obj.get("averageWindSpeed"))
        maximum_wind_speed = from_float(obj.get("maximumWindSpeed"))
        wind_direction = from_str(obj.get("windDirection"))
        precipitation = from_str(obj.get("precipitation"))
        precipitation_rate = from_float(obj.get("precipitationRate"))
        visibility = from_float(obj.get("visibility"))
        last_update = from_datetime(obj.get("lastUpdate"))
        return AtmosphericSensor(air_temperature, dewpoint_temperature, humidity, average_wind_speed,
                                 maximum_wind_speed, wind_direction, precipitation, precipitation_rate, visibility,
                                 last_update)

    def to_dict(self) -> dict:
        result: dict = {"airTemperature": to_float(self.air_temperature),
                        "dewpointTemperature": to_float(self.dewpoint_temperature), "humidity": to_float(self.humidity),
                        "averageWindSpeed": to_float(self.average_wind_speed),
                        "maximumWindSpeed": to_float(self.maximum_wind_speed),
                        "windDirection": from_str(self.wind_direction), "precipitation": from_str(self.precipitation),
                        "precipitationRate": to_float(self.precipitation_rate), "visibility": to_float(self.visibility),
                        "lastUpdate": self.last_update.isoformat()}
        return result


@dataclass
class SurfaceSensor:
    name: str
    status: str
    surface_temperature: float
    sub_surface_temperature: float
    last_update: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'SurfaceSensor':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        status = from_str(obj.get("status"))
        surface_temperature = from_float(obj.get("surfaceTemperature"))
        sub_surface_temperature = from_float(obj.get("subSurfaceTemperature"))
        last_update = from_datetime(obj.get("lastUpdate"))
        return SurfaceSensor(name, status, surface_temperature, sub_surface_temperature, last_update)

    def to_dict(self) -> dict:
        result: dict = {"name": from_str(self.name), "status": from_str(self.status),
                        "surfaceTemperature": to_float(self.surface_temperature),
                        "subSurfaceTemperature": to_float(self.sub_surface_temperature),
                        "lastUpdate": self.last_update.isoformat()}
        return result


@dataclass
class WeatherSensorSite(BaseModel):
    """
    WeatherSensorSite is a class for storing weather sensor site objects.

    Attributes:
    severe: A boolean indicating if the weather conditions are severe.
    condition: The current weather condition at the site.
    average_air_temperature: The average air temperature at the site.
    atmospheric_sensors: A list of atmospheric sensors at the site.
    surface_sensors: A list of surface sensors at the site.
    """

    severe: bool
    condition: Optional[str]
    average_air_temperature: str
    atmospheric_sensors: List[AtmosphericSensor]
    surface_sensors: List[SurfaceSensor]

    def __init__(
            self,
            links: List[Link],
            id: str,
            latitude: float,
            longitude: float,
            location: str,
            description: Optional[str],
            severe: bool,
            condition: Optional[str],
            average_air_temperature: str,
            atmospheric_sensors: List[AtmosphericSensor],
            surface_sensors: List[SurfaceSensor]
    ):
        """
        Initializes the WeatherSensorSite object with common fields and weather-specific fields.
        :param links: A list of Link objects associated with the weather sensor site.
        :param id: The ID of the weather sensor site.
        :param latitude: The latitude of the weather sensor site.
        :param longitude: The longitude of the weather sensor site.
        :param location: The location of the weather sensor site.
        :param description: A description of the weather sensor site.
        :param severe: A boolean indicating if the weather conditions are severe.
        :param condition: The current weather condition at the site.
        :param average_air_temperature: The average air temperature recorded at the site.
        :param atmospheric_sensors: A list of AtmosphericSensor objects.
        :param surface_sensors: A list of SurfaceSensor objects.
        """
        super().__init__(links, id, latitude, longitude, location, description)  # Call BaseModel's init
        self.severe = severe
        self.condition = condition
        self.average_air_temperature = average_air_temperature
        self.atmospheric_sensors = atmospheric_sensors
        self.surface_sensors = surface_sensors

    @staticmethod
    def from_dict(obj: Any) -> 'WeatherSensorSite':
        """
        Converts a dictionary into a WeatherSensorSite object.
        :param obj: A dictionary representing a WeatherSensorSite.
        :return: A WeatherSensorSite object.
        """
        base_model = BaseModel.from_base_dict(obj)  # Get common fields using BaseModel
        severe = from_bool(obj.get("severe"))
        condition = from_str(obj.get("condition"))
        average_air_temperature = from_str(obj.get("averageAirTemperature"))
        atmospheric_sensors = from_list(AtmosphericSensor.from_dict, obj.get("atmosphericSensors"))
        surface_sensors = from_list(SurfaceSensor.from_dict, obj.get("surfaceSensors"))
        return WeatherSensorSite(base_model.links, base_model.id, base_model.latitude, base_model.longitude,
                                 base_model.location, base_model.description, severe, condition, average_air_temperature,
                                 atmospheric_sensors, surface_sensors)

    def to_dict(self) -> dict:
        """
        Converts the WeatherSensorSite object into a dictionary.
        :return: A dictionary representation of the WeatherSensorSite object.
        """
        result = self.base_to_dict()  # Get common fields from BaseModel
        result.update({
            "severe": from_bool(self.severe),
            "condition": from_str(self.condition),
            "averageAirTemperature": from_str(self.average_air_temperature),
            "atmosphericSensors": from_list(lambda x: to_class(AtmosphericSensor, x), self.atmospheric_sensors),
            "surfaceSensors": from_list(lambda x: to_class(SurfaceSensor, x), self.surface_sensors)
        })
        return result

