from datetime import datetime

from pydantic import BaseModel, HttpUrl


class BasePage(BaseModel):
    title: str
    author: str
    published_at: datetime
    content: str
    url: HttpUrl
    tags: list[str]
