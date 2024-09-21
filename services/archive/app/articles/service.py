from uuid import UUID

from app.articles.model import Article
from app.articles.repository import ArticlesRepositoryInterface
from app.common.repository import PaginationResult
from logger import logger


class ArticlesService:
    def __init__(
            self,
            data_layer_entrypoint: ArticlesRepositoryInterface
    ):
        self.data_layer_entrypoint = data_layer_entrypoint

    def find_by_id(self, id: int) -> Article | None:
        logger.debug("Retrieving article by id.", extra={"id": id})
        article = self.data_layer_entrypoint.find_by_id(id)
        if article:
            logger.info(
                "Articles retrieved.",
                extra={
                    "article": article.model_dump()
                }
            )
        else:
            logger.warning(
                "Article not found",
                extra={"id": id}
            )
        return self.data_layer_entrypoint.find_by_id(id)

    def find_all(self, page: int = 1, items_per_page: int = 20) -> PaginationResult:
        logger.debug("Retrieving all the current articles available, paginated.")
        pagination_result = self.data_layer_entrypoint.find_all(page=page, items_per_page=items_per_page)

        logger.info(
            "Articles paginated retrieved.",
            extra={
                "total_articles": pagination_result.total_items,
                "page": pagination_result.page,
                "items_per_page": pagination_result.items_per_page,
                "items": pagination_result.items
            }
        )
        return pagination_result
