import json
from urllib.parse import urlencode

from app.api_resource import SendableResource


class CoindeskLatestNews(SendableResource):
    ACTION = "/api/v3/content/fetch/please-stop"
    METHOD = "GET"

    def __init__(
            self,
            size: int = 20,
            page: int = 1,
            language: str = "en",
            format: str = "timeline"
    ):
        self.language = language
        self.format = format  # Removed comma here
        self.size = size
        self.page = page

    def get_payload(self) -> dict | None:
        return None

    def get_action(self) -> str:
        params = {
            "language": self.language,
            "format": self.format,
            "size": self.size,
            "page": self.page,
        }
        json_query = json.dumps(params)
        action_url = f"{self.ACTION}?query={json_query}"
        return action_url
