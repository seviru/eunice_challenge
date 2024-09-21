from abc import ABC, abstractmethod

from requests import Response

from app.api_client.exception import RequestException
from app.api_resource import SendableResource
from logger import logger


class BaseClient(ABC):
    @abstractmethod
    def send(self, resource: SendableResource) -> dict:
        raise NotImplementedError

    @staticmethod
    def _handle_response(response: Response) -> dict:
        if response.status_code >= 300:
            logger.warning(
                "Client request failed",
                extra={
                    "status_code": response.status_code,
                    "headers": str(response.headers),
                    "method": response.request.method,
                    "url": response.request.url,
                    "response_text": response.text
                }
            )

            raise RequestException(
                response.status_code,
                str(response.headers),
                response.request.method,
                response.request.url,
                response.text
            )

        logger.debug(
            "Successful API request",
            extra={
                "method": response.request.method,
                "url": response.request.url,
                "payload": response.request.body,
                "response_status": response.status_code,
                "response_data": response.text
            }
        )
        return response.json()
