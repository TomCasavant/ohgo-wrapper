from dataclasses import dataclass
from datetime import datetime
from typing import List, Any

from .base_model import BaseModel
from .models import Link, from_list, from_str, from_float, from_datetime, to_float, to_class


@dataclass
class Construction(BaseModel):
    """
    Construction is a class for storing construction information.

    Attributes:
    category: The category of the construction work.
    direction: The direction related to the construction site.
    district: The district where the construction is taking place (can be None).
    route_name: The name of the route where the construction is located.
    status: The current status of the construction work.
    start_date: The start date of the construction work.
    end_date: The expected end date of the construction work.
    """

    category: str
    direction: str
    district: str
    route_name: str
    status: str
    start_date: datetime
    end_date: datetime

    def __init__(
            self,
            links: List[Link],
            id: str,
            latitude: float,
            longitude: float,
            location: str,
            description: str,
            category: str,
            direction: str,
            district: str,
            route_name: str,
            status: str,
            start_date: datetime,
            end_date: datetime
    ):
        """
        Initializes the Construction object.
        :param links: A list of Link objects associated with the construction work.
        :param id: The ID of the construction work.
        :param latitude: The latitude of the construction site.
        :param longitude: The longitude of the construction site.
        :param location: The location where the construction is happening.
        :param description: A description of the construction work.
        :param category: The category of the construction work.
        :param direction: The direction associated with the construction work.
        :param district: The district where the construction is located.
        :param route_name: The name of the route affected by the construction work.
        :param status: The current status of the construction work.
        :param start_date: The start date of the construction work.
        :param end_date: The expected end date of the construction work.
        """
        super().__init__(links, id, latitude, longitude, location, description)  # Initialize common fields from BaseModel
        self.category = category
        self.direction = direction
        self.district = district
        self.route_name = route_name
        self.status = status
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def from_dict(obj: Any) -> "Construction":
        """
        Converts a dictionary into a Construction object.
        :param obj: A dictionary representing a Construction object.
        :return: A Construction object.
        """
        base_model = BaseModel.from_base_dict(obj)  # Parse common fields using BaseModel
        category = from_str(obj.get("category"))
        direction = from_str(obj.get("direction"))
        district = from_str(obj.get("district"))
        route_name = from_str(obj.get("routeName"))
        status = from_str(obj.get("status"))
        start_date = from_datetime(obj.get("startDate"))
        end_date = from_datetime(obj.get("endDate"))
        return Construction(
            base_model.links, base_model.id, base_model.latitude, base_model.longitude, base_model.location,
            base_model.description, category, direction, district, route_name, status, start_date, end_date
        )

    def to_dict(self) -> dict:
        """
        Converts the Construction object into a dictionary.
        :return: A dictionary representation of the Construction object.
        """
        result = self.base_to_dict()  # Get common fields from BaseModel
        result.update({
            "category": from_str(self.category),
            "direction": from_str(self.direction),
            "district": from_str(self.district),
            "routeName": from_str(self.route_name),
            "status": from_str(self.status),
            "startDate": self.start_date.isoformat(),
            "endDate": self.end_date.isoformat()
        })
        return result

