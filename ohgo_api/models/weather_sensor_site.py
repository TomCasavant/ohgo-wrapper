from dataclasses import dataclass
from datetime import datetime
from typing import List, Any

from ohgo_api.models.models import from_list, from_str, Link, from_float, to_class, to_float, from_bool, \
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
class WeatherSensorSite:
    links: List[Link]
    id: int
    latitude: float
    longitude: float
    location: str
    description: None
    severe: bool
    condition: None
    average_air_temperature: str
    atmospheric_sensors: List[AtmosphericSensor]
    surface_sensors: List[SurfaceSensor]

    @staticmethod
    def from_dict(obj: Any) -> 'WeatherSensorSite':
        assert isinstance(obj, dict)
        links = from_list(Link.from_dict, obj.get("links"))
        id = int(from_str(obj.get("id")))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        location = from_str(obj.get("location"))
        description = from_str(obj.get("description"))
        severe = from_bool(obj.get("severe"))
        condition = from_str(obj.get("condition"))
        average_air_temperature = from_str(obj.get("averageAirTemperature"))
        atmospheric_sensors = from_list(AtmosphericSensor.from_dict, obj.get("atmosphericSensors"))
        surface_sensors = from_list(SurfaceSensor.from_dict, obj.get("surfaceSensors"))
        return WeatherSensorSite(links, id, latitude, longitude, location, description, severe, condition,
                                 average_air_temperature, atmospheric_sensors, surface_sensors)

    def to_dict(self) -> dict:
        result: dict = {"links": from_list(lambda x: to_class(Link, x), self.links), "id": from_str(str(self.id)),
                        "latitude": to_float(self.latitude), "longitude": to_float(self.longitude),
                        "location": from_str(self.location), "description": from_str(self.description),
                        "severe": from_bool(self.severe), "condition": from_str(self.condition),
                        "averageAirTemperature": from_str(self.average_air_temperature),
                        "atmosphericSensors": from_list(lambda x: to_class(AtmosphericSensor, x),
                                                        self.atmospheric_sensors),
                        "surfaceSensors": from_list(lambda x: to_class(SurfaceSensor, x), self.surface_sensors)}
        return result
