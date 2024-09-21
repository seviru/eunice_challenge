import os

from pydantic import HttpUrl

from app.api_client import CoindeskClient
from app.api_resource import CoindeskLatestNews
from app.url_retriever import UrlRetrieverInterface

from typing import TypedDict

from logger import logger


class ImageSource(TypedDict):
    webp: str
    jpeg: str


class ImageDetails(TypedDict):
    src: str
    width: int
    height: int
    sources: ImageSource


class Image(TypedDict):
    alt: str
    type: str
    mobile: ImageDetails
    tablet: ImageDetails
    desktop: ImageDetails


class News(TypedDict):
    _id: str
    url: str
    title: str
    description: str
    date: str
    image: Image
    category: str


class LastCoindeskArticlesRetriever(UrlRetrieverInterface):
    # TODO: Move this to an env variable, possible different for prod and dev
    COINDESK_URL = os.getenv("COINDESK_URL") or 'https://www.coindesk.com'

    def __init__(self,
                 number_of_articles: int,
                 exclude_categories: list[str] | None = None,
                 coindesk_api_client: CoindeskClient = CoindeskClient(),
                 max_pages_tried: int = 100,
                 ):
        self.number_of_articles = number_of_articles
        self.exclude_categories = [
            category.lower() for category in
            exclude_categories
        ] if exclude_categories is not None else []
        self.coindesk_client = coindesk_api_client
        self.max_pages_tried = max_pages_tried

    def retrieve_urls(self) -> list[HttpUrl]:
        """"""
        urls = []
        current_pages_tried = 0
        news = None

        logger.info(
            "Retrieving Coindesk articles matching search criteria",
            extra={
                "number_of_articles": self.number_of_articles,
                "categories_excluded": self.exclude_categories
            }
        )

        while len(urls) < self.number_of_articles and current_pages_tried < self.max_pages_tried:
            current_pages_tried += 1
            # TODO: Create a DTO to contain the response instead of accessing dictioanry fields
            news: list[News] | None = self.coindesk_client.send(
                CoindeskLatestNews(
                    page=current_pages_tried
                )
            )["items"]

            if news:
                for i, article in enumerate(news):
                    url = f"{self.COINDESK_URL}{article['url']}"
                    if article["category"].lower() not in self.exclude_categories:
                        logger.debug("Article matching criteria found", extra={"url": url})
                        urls.append(url)

                        if len(urls) >= self.number_of_articles:
                            break
                    else:
                        logger.debug("Article not matching criteria found", extra={"url": url})

        logger.info("Articles found for search parameters", extra={"amount": len(urls)})

        return urls
