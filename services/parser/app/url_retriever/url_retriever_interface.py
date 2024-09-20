from abc import ABC, abstractmethod

from pydantic import HttpUrl


class UrlRetrieverInterface(ABC):
    @abstractmethod
    def retrieve_urls(self) -> list[HttpUrl]:
        raise NotImplementedError
