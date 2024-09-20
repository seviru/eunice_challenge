import os

import requests

from app.api_client import BaseClient
from app.api_resource import SendableResource


class CoindeskClient(BaseClient):
    def __init__(
            self,
            # TODO: Move this to env variable
            coindesk_base_api_url=os.getenv("COINDESK_BASE_API_URL") or "https://www.coindesk.com/pf"
    ):
        self._coindesk_base_api_url = coindesk_base_api_url

    def send(self, resource: SendableResource) -> dict:
        method = resource.get_method()
        payload = resource.get_payload()
        url = f"{self._coindesk_base_api_url}{resource.get_action()}"

        response = requests.request(method, url, json=payload)

        return self._handle_response(response)
