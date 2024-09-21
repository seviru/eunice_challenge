from abc import ABC, abstractmethod

from app.model import BasePage


class PageStorerInterface(ABC):
    @abstractmethod
    def store_page(self, page: BasePage) -> None:
        raise NotImplementedError
