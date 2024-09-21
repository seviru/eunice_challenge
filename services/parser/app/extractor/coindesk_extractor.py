from datetime import datetime

import pytz
from pydantic import HttpUrl

import requests
from bs4 import BeautifulSoup

from app import BasePage
from app.extractor import PageExtractorInterface
from logger import logger


class CoindeskExtractor(PageExtractorInterface):
    def extract_page_info(self, url: HttpUrl) -> BasePage:
        logger.info("Retrieving article information from url", extra={"url": str(url)})

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        title = self._extract_title(soup)
        author = self._extract_author(soup)
        published_at = self._extract_publishing_date(soup)
        content = self._extract_content(soup)
        tags = self._extract_tags(soup)

        logger.debug(
            "Article information retrieved",
            extra={
                "title": title,
                "author": author,
                "published_at": published_at.strftime("%m-%d-%Y %H:%M:%S"),
                "content": content,
                "tags": tags
            }
        )

        return BasePage(
            title=title,
            author=author,
            published_at=published_at,
            content=content,
            url=url,
            tags=tags
        )

    def _extract_title(self, soup: BeautifulSoup) -> str | None:
        # First try to get the OpenGraph title
        meta_title = soup.find('meta', {'property': 'og:title'})
        if meta_title:
            return meta_title['content']

        # If og:title not present, get the <title> text
        page_title = soup.find('title')
        if page_title:
            return page_title.text

        # Return None if no title could be extracted
        return None

    def _extract_author(self, soup: BeautifulSoup) -> str | None:
        meta_author = soup.find('meta', {'property': 'article:author'})
        if meta_author:
            return meta_author['content']

        return None

    def _extract_publishing_date(self, soup: BeautifulSoup) -> datetime | None:
        meta_date = soup.find('meta', {'property': 'article:published_time'})
        if meta_date:
            date_string = meta_date['content']
            date_format_with_microseconds = '%Y-%m-%dT%H:%M:%S.%fZ'
            date_format_without_microseconds = '%Y-%m-%dT%H:%M:%SZ'
            try:
                date_object = datetime.strptime(date_string, date_format_with_microseconds)
            except ValueError:
                date_object = datetime.strptime(date_string, date_format_without_microseconds)

            # To save this datetime in UTC timezone
            date_object = date_object.replace(tzinfo=pytz.UTC)
            return date_object

        return None

    def _extract_content(self, soup: BeautifulSoup) -> str:
        section = soup.find('section', attrs={'class': 'at-body'})
        return ' '.join([p.text for p in section.find_all('p')])

    def _extract_tags(self, soup: BeautifulSoup) -> list[str]:
        meta_tags = soup.find('meta', {'property': 'article:tag'})
        if meta_tags:
            # Split on comma and strip whitespace
            tags = [tag.strip() for tag in meta_tags['content'].split(',')]
            return tags
        return []
