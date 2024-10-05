from typing import Union

from ohgo.exceptions import OHGOException
from ohgo.rest_adapter import RestAdapter
from PIL import Image


class ImageHandler:
    """
    ImageHandler is a class for handling image fetching from URLs

    Attributes:
    _rest_adapter: RestAdapter for making HTTP requests to the OHGO API

    Methods:
    fetch: Fetches an image from a URL
    """

    def __init__(self, rest_adapter: RestAdapter):
        """
        Constructor for ImageHandler. Initializes the RestAdapter for making HTTP requests to the OHGO API.
        :param rest_adapter: RestAdapter for making HTTP requests to the OHGO API
        """
        self._rest_adapter = rest_adapter

    def fetch(self, url: str) -> Union[Image.Image, None]:
        """
        Fetches an image from a URL. Returns None if the image cannot be fetched.
        :param url: A string URL to fetch the image from.
        :return: A PIL Image object
        """
        try:
            image_bytes = self._rest_adapter.get_image(url)
        except OHGOException:
            return None
        return Image.open(image_bytes)
