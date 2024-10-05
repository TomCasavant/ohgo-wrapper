import requests
import requests.packages
from typing import Dict
from .exceptions import OHGOException
from ohgo.models.models import Result
from json import JSONDecodeError
import logging
from io import BytesIO


class RestAdapter:
    """
    RestAdapter is a class for making HTTP requests to the OHGO API

    Attributes:
    url: The base URL of the OHGO API
    _api_key: The API key for the OHGO API
    _ssl_verify: Whether to verify SSL certificates
    _logger: A logger for logging messages

    Methods:
    get: Makes a GET request to the OHGO API
    get_image: Fetches an image from a URL
    _do: Makes a request to the OHGO API
    """
    def __init__(
            self,
            hostname: str,
            api_key: str = "",
            ver: str = "v1",
            ssl_verify: bool = True,
            logger: logging.Logger = None,
    ):
        """
        Constructor for RestAdapter. Initializes the base URL, API key, SSL verification, and logger.
        :param hostname: hostname of the OHGO API. Almost always "publicapi.ohgo.com"
        :param api_key: API key for the OHGO API
        :param ver: Version of the API to use. Defaults to "v1"
        :param ssl_verify: Whether to verify SSL certificates. Defaults to True
        :param logger: (optional) A logger to use for logging. Defaults to None. A new logger will be created if None.
        """

        self.url = "https://{}/api/{}/".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

    def get(self, endpoint: str, ep_params: Dict = {}, fetch_all=False) -> Result:
        """
        Makes a GET request to the OHGO API
        :param endpoint: The endpoint to make the request to
        :param ep_params: The parameters to pass to the endpoint
        :param fetch_all: Whether to fetch all results. Defaults to False. Recommended to use page-all param instead.
        :return: A Result object
        """
        result = self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)
        if fetch_all:
            # Fetch all results by following the next page links
            next_page_url = result.next_page
            while next_page_url:
                page_result = self._do(http_method="GET", endpoint=next_page_url, ep_params=ep_params)
                result.data.extend(page_result.data)
                next_page_url = page_result.next_page
        return result

    def get_image(self, url) -> BytesIO:
        """
        Fetches an image from a URL
        :param url: The URL to fetch the image from
        :return: A BytesIO object containing the image
        """
        try:
            response = requests.get(url, verify=self._ssl_verify)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            self._logger.error(f"Error while fetching image from {url}: {e}")
            raise OHGOException(f"Failed to fetch image from {url}") from e

    def _do(
            self, http_method: str, endpoint: str, ep_params: Dict = {}, data: Dict = {}
    ) -> Result:
        """
        Helper method that makes a request to the OHGO API
        :param http_method: The HTTP method to use. Currently, OHGO only supports GET
        :param endpoint: The endpoint to make the request to
        :param ep_params: The parameters to pass to the endpoint
        :param data: The data to pass to the endpoint.
        :return: A Result object
        """
        full_url = endpoint if endpoint.startswith('http') else self.url + endpoint
        headers = {
            "Authorization": f"APIKEY {self._api_key}"
        }
        ep_params = {k: v for k, v in ep_params.items() if v is not None}
        print(http_method, endpoint, ep_params, data)
        print(full_url)
        try:
            response = requests.request(
                method=http_method,
                url=full_url,
                verify=self._ssl_verify,
                headers=headers,
                params=ep_params,
                json=data,
            )
        except (ValueError, JSONDecodeError) as e:
            raise OHGOException("Request failed.") from e
        data_out = response.json()
        if 299 >= response.status_code >= 200:
            # Successful request
            result = Result(
                status_code=response.status_code,
                message=response.reason,
                data=data_out,
            )

            for query_filter in result.rejected_filters:
                # OHGO rejected a filter, log a warning
                self._logger.warning(f" Error: {query_filter['error']} - {query_filter['key']}:{query_filter['value']}")

            return result
        raise OHGOException(f"{response.status_code}: {response.reason}")
