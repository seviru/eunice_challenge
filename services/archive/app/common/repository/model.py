from pydantic import BaseModel

from app.common.repository import BaseEntity


class PaginationResult(BaseModel):
    page: int
    items_per_page: int
    total_items: int
    total_pages: int
    items: list[BaseEntity]


class ConnectionInfo(BaseModel):
    dbname: str
    user: str
    host: str
    password: str
    port: int = 5432
