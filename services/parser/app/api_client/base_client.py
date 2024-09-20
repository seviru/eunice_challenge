from abc import ABC, abstractmethod

from requests import Response

from app.api_client.exceptions import RequestException
from app.api_resource import SendableResource


class BaseClient(ABC):
    @abstractmethod
    def send(self, resource: SendableResource) -> dict:
        raise NotImplementedError

    @staticmethod
    def _handle_response(response: Response) -> dict:
        if response.status_code >= 300:
            raise RequestException(
                response.status_code,
                str(response.headers),
                response.request.method,
                response.request.url,
                response.text
            )

        return response.json()
