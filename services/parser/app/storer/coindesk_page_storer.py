import psycopg2
from psycopg2 import sql
from pydantic import BaseModel

from app import BasePage
from app.storer import PageStorerInterface


class ConnectionInfo(BaseModel):
    dbname: str
    user: str
    host: str
    password: str
    port: int = 5432


class CoindeskPageStorer(PageStorerInterface):
    def __init__(self, connection_info: ConnectionInfo):
        self._connection_info = connection_info

    def _get_connection(self):
        conn = psycopg2.connect(**self._connection_info.model_dump())
        conn.autocommit = True
        return conn

    def store_page(self, page: BasePage) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                insert = sql.SQL(
                    """
                    INSERT INTO articles 
                    (title, author, published_at, content, url, tags) 
                    VALUES 
                    (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO NOTHING
                    """
                )
                cursor.execute(
                    insert, (
                        page.title,
                        page.author,
                        page.published_at,
                        page.content,
                        str(page.url),
                        page.tags
                    )
                )
