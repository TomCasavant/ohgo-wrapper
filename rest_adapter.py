import requests
import requests.packages
from typing import List, Dict

class RestAdapter:
    def __init__(self, hostname: str, api_key: str = '', ver: str = 'v1'), ssl_verify: bool = True):
        self.url = "https://{}/{}/".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

    def get(self, endpoint: str, ep_params: Dict = None) -> List[Dict]:
        full_url = self.url + endpoint
        headers = {'x-api-key' : self._api_key}
        response = requests.get(url=full_url, verify=self._ssl_verify, headers=headers, params=ep_params)
        data_out = response.json()
        if response.status_code >= 200 and response.status_code <= 299:
            return data_out
        raise Exception(data_out["message"])
