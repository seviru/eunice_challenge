import os

from pydantic import HttpUrl

from app.api_client import CoindeskClient
from app.api_client.exception import CoindeskRequestException
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
                 ):
        self.number_of_articles = number_of_articles
        self.exclude_categories = [
            category.lower() for category in
            exclude_categories
        ] if exclude_categories is not None else []
        self.coindesk_client = coindesk_api_client

    def retrieve_urls(self) -> list[HttpUrl]:
        urls = []
        current_pages_tried = 0

        logger.info(
            "Retrieving Coindesk articles matching search criteria",
            extra={
                "number_of_articles": self.number_of_articles,
                "categories_excluded": self.exclude_categories
            }
        )
        while len(urls) < self.number_of_articles:
            current_pages_tried += 1
            try:
                # TODO: Create a DTO to contain the response instead of accessing dictionary fields
                news: list[News] | None = self.coindesk_client.send(
                    CoindeskLatestNews(
                        page=current_pages_tried
                    )
                )["items"]
            except CoindeskRequestException as e:
                logger.warning("Error while trying request. Processing current stored URLs.", extra={"exception": str(e)})
                break

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
        logger.debug(
            f"Number of articles {self.number_of_articles} /// current {len(urls)} /// page tried {current_pages_tried}"
        )
        logger.info("Articles found for search parameters", extra={"amount": len(urls)})
        logger.info("Urls retrieved", extra={"urls": urls})

        return urls
