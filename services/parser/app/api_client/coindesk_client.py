import os

import requests

from app.api_client import BaseClient
from app.api_client.exception import RequestException, CoindeskRequestException
from app.api_resource import SendableResource
from logger import logger


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
        logger.info(f"URL: {url}")

        response = requests.request(method, url, json=payload)

        try:
            logger.debug("Executing request to Coindesk API")
            handled_response = self._handle_response(response)
            logger.debug("Successful request to Coindesk API")

        except RequestException as e:
            logger.warning("Error while processing request to Coindesk API")
            raise CoindeskRequestException.from_request_exception(e) from e

        return handled_response
