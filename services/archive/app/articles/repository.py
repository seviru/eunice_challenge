from abc import abstractmethod, ABC
from contextlib import contextmanager
from uuid import UUID

import psycopg2
from psycopg2.extras import DictCursor

from app.articles.model import Article
from app.common.model import ConnectionInfo
from app.common.repository import RepositoryInterface, PaginationResult
from logger import logger


class ArticlesRepositoryInterface(RepositoryInterface[Article], ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> Article | None:
        pass

    @abstractmethod
    def find_all(self, page: int, items_per_page: int) -> PaginationResult:
        pass


class ArticlesRepository(ArticlesRepositoryInterface):
    def __init__(self, db_credentials: ConnectionInfo):
        self.db_credentials = db_credentials

    def _connect(self):
        self.conn = psycopg2.connect(**self.db_credentials.model_dump())
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)

    def _disconnect(self):
        self.cursor.close()
        self.conn.close()

    def _execute(self, query, data):
        self.cursor.execute(query, data)

    def _commit(self):
        self.conn.commit()

    def _parse_record(self, record) -> Article:
        column_names = ['id', 'title', 'author', 'published_at', 'content', 'url', 'tags']
        article_data = {k: v for k, v in zip(column_names, record)}
        return Article.model_validate(article_data)

    @contextmanager
    def db_operation(self, query, data, commit=False):
        self._connect()
        try:
            self._execute(query, data)
            if commit:
                self._commit()
            yield self.cursor
        finally:
            self._disconnect()

    def find_by(self, **kwargs) -> Article | None:
        query = "SELECT * FROM articles WHERE " + ' AND '.join([f"{k} = %s" for k in kwargs.keys()])
        with self.db_operation(query, tuple(kwargs.values())) as cursor:
            record = cursor.fetchone()
            if record:
                return self._parse_record(record)
        return None

    def save(self, model: Article,  commit: bool = False) -> None:
        query = """INSERT INTO articles (title, author, published_at, content, url, tags) \
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        data = (model.title, model.author, model.published_at, model.content, model.url, model.tags)
        with self.db_operation(query, data, commit=commit):
            pass

    def find_all(self, page: int, items_per_page: int) -> PaginationResult:
        logger.debug("Requesting all the current articles available, paginated.")

        offset = (page - 1) * items_per_page
        with self.db_operation("SELECT COUNT(*) FROM articles", tuple()) as cursor:
            total_items = cursor.fetchone()[0]
        with self.db_operation(
                "SELECT * FROM articles ORDER BY published_at DESC LIMIT %s OFFSET %s",
                (items_per_page, offset)
        ) as cursor:
            records = cursor.fetchall()

        logger.debug(f"Articles retrieved, paginated.{records}", extra={"records": records})
        articles = [self._parse_record(record) for record in records]

        pagination = PaginationResult(
            page=page,
            items_per_page=items_per_page,
            total_items=total_items,
            total_pages=-(-total_items // items_per_page),  # equivalent to math.ceil(total_items / items_per_page)
            items=articles
        )

        return pagination

    def find_by_id(self, id: int) -> Article | None:
        return self.find_by(id=id)
