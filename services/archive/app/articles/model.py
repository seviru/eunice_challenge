from datetime import datetime

from pydantic import HttpUrl

from app.common.repository import BaseEntity


class Article(BaseEntity):
    title: str
    author: str
    published_at: datetime
    content: str
    url: HttpUrl
    tags: list[str]
