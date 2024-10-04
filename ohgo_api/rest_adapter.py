import requests
import requests.packages
from typing import List, Dict
from .exceptions import OHGoException
from .models import Result
from json import JSONDecodeError
import logging
from io import BytesIO

class RestAdapter:
    def __init__(
        self,
        hostname: str,
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self.url = "https://{}/api/{}/".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

    def get(self, endpoint: str, ep_params: Dict = {}, fetch_all=False) -> Result:
        result = self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)
        if fetch_all:
            next_page_url = result.next_page
            while next_page_url:
                page_result = self._do(http_method="GET", endpoint=next_page_url, ep_params=ep_params)
                result.data.extend(page_result.data)
                next_page_url = page_result.next_page
        return result

    def get_image(self, url) -> BytesIO:
        try:
            response = requests.get(url, verify=self._ssl_verify)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            self._logger.error(f"Error while fetching image from {url}: {e}")
            raise OHGoException(f"Failed to fetch image from {url}") from e

    def _do(
        self, http_method: str, endpoint: str, ep_params: Dict = {}, data: Dict = {}
    ) -> Result:
        full_url = endpoint if endpoint.startswith('http') else self.url + endpoint
        headers = {
            "Authorization" : f"APIKEY {self._api_key}"
        }
        ep_params = { k: v for k, v in ep_params.items() if v is not None }
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
            raise OHGoException("Request failed.") from e
        data_out = response.json()
        if 299 >= response.status_code >= 200:
            result = Result(
                status_code=response.status_code,
                message=response.reason,
                data=data_out,
            )

            for query_filter in result.rejected_filters:
                self._logger.warning(f" Error: {query_filter['error']} - {query_filter['key']}:{query_filter['value']}")

            return result
        raise OHGoException(f"{response.status_code}: {response.reason}")
