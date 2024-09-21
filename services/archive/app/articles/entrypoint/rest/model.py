from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from app.articles.model import Article


class ArticlesPaginatedResponseModel(BaseModel):
    page: int
    items_per_page: int
    total_items: int
    total_pages: int
    items: list[Article]


class ArticleResponse(BaseModel):
    id: int
    title: str
    author: str
    published_at: datetime
    content: str
    url: HttpUrl
    tags: list[str]