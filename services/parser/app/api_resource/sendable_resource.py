from abc import ABC, abstractmethod


class BaseResource(ABC):
    @abstractmethod
    def get_payload(self) -> dict | None:
        pass


class SendableResource(BaseResource, ABC):
    ACTION = None
    METHOD = None

    def get_method(self) -> str:
        if not self.METHOD:
            raise NotImplementedError

        return self.METHOD

    def get_action(self) -> str:
        if not self.ACTION:
            raise NotImplementedError

        return self.ACTION
