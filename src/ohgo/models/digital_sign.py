from dataclasses import dataclass
from typing import List, Any

from .base_model import BaseModel
from .models import from_list, from_str, from_float, to_float, to_class, Link


@dataclass
class DigitalSign(BaseModel):
    """
    DigitalSign is a class for storing digital sign objects.

    Attributes:
    sign_type_name: The name/type of the digital sign.
    messages: A list of messages displayed by the sign.
    image_urls: A list of URLs for images associated with the digital sign.
    """

    sign_type_name: str
    messages: List[str]
    image_urls: List[Any]

    def __init__(
            self,
            links: List[Link],
            id: str,
            latitude: float,
            longitude: float,
            location: str,
            description: str,
            sign_type_name: str,
            messages: List[str],
            image_urls: List[Any]
    ):
        """
        Initializes the DigitalSign object with common fields and sign-specific fields.
        :param links: A list of Link objects associated with the sign.
        :param id: The ID of the sign.
        :param latitude: The latitude of the sign's location.
        :param longitude: The longitude of the sign's location.
        :param location: The location of the sign.
        :param description: The description of the sign.
        :param sign_type_name: The name or type of the digital sign.
        :param messages: A list of messages displayed by the digital sign.
        :param image_urls: A list of image URLs associated with the digital sign.
        """
        super().__init__(links, id, latitude, longitude, location, description)  # Call BaseModel's init
        self.sign_type_name = sign_type_name
        self.messages = messages
        self.image_urls = image_urls

    @staticmethod
    def from_dict(obj: Any) -> 'DigitalSign':
        """
        Converts a dictionary into a DigitalSign object.
        :param obj: A dictionary representing a DigitalSign.
        :return: A DigitalSign object.
        """
        base_model = BaseModel.from_base_dict(obj)  # Get common fields using BaseModel
        sign_type_name = from_str(obj.get("signTypeName"))
        messages = from_list(from_str, obj.get("messages"))
        image_urls = from_list(lambda x: x, obj.get("imageUrls"))
        return DigitalSign(base_model.links, base_model.id, base_model.latitude, base_model.longitude,
                           base_model.location, base_model.description, sign_type_name, messages, image_urls)

    def to_dict(self) -> dict:
        """
        Converts the DigitalSign object into a dictionary.
        :return: A dictionary representation of the DigitalSign object.
        """
        result = self.base_to_dict()  # Get common fields from BaseModel
        result.update({
            "signTypeName": from_str(self.sign_type_name),
            "messages": from_list(from_str, self.messages),
            "imageUrls": from_list(lambda x: x, self.image_urls)
        })
        return result


