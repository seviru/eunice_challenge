from abc import ABC, abstractmethod

from pydantic import HttpUrl

from app.model import BasePage


class PageExtractorInterface(ABC):
    @abstractmethod
    def extract_page_info(self, url: HttpUrl) -> BasePage:
        raise NotImplementedError
