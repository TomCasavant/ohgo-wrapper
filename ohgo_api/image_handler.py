import requests
from ohgo_api.rest_adapter import RestAdapter
from PIL import Image


class ImageHandler:
    """
    ImageHandler is a class for handling image fetching from URLs

    Attributes:
    _rest_adapter: RestAdapter for making HTTP requests to the OHGo API

    Methods:
    fetch: Fetches an image from a URL
    """
    def __init__(self, rest_adapter: RestAdapter):
        """
        Constructor for ImageHandler. Initializes the RestAdapter for making HTTP requests to the OHGo API.
        :param rest_adapter: RestAdapter for making HTTP requests to the OHGo API
        """
        self._rest_adapter = rest_adapter

    def fetch(self, url: str) -> Image.Image:
        """
        Fetches an image from a URL
        :param url: A string URL to fetch the image from.
        :return: A PIL Image object
        """
        return Image.open(self._rest_adapter.get_image(url))
