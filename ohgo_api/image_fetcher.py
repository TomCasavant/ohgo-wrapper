import requests
from ohgo_api.rest_adapter import RestAdapter
from PIL import Image

class ImageFetcher:
    def __init__(self, rest_adapter: RestAdapter):
        self._rest_adapter = rest_adapter

    def fetch(self, url: str) -> Image.Image:
        return Image.open(self._rest_adapter.get_image(url))
