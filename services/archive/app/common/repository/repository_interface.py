from abc import ABC
from typing import TypeVar, Generic
from uuid import UUID

from pydantic import BaseModel


class BaseEntity(BaseModel):
    id: int


BASE = TypeVar("BASE", bound=BaseEntity)


class RepositoryInterface(ABC, Generic[BASE]):
    def find_by(self, **kwargs) -> BASE:
        pass

    def save(self, model: BASE, commit: bool = False) -> None:
        pass
