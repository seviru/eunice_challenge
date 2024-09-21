from fastapi import APIRouter, Query, Path, HTTPException
from starlette import status

from app.articles import articles_service
from app.articles.entrypoint.rest.model import ArticlesPaginatedResponseModel, ArticleResponse

router = APIRouter(prefix="/api/articles", tags=["articles"], dependencies=[])


@router.get("", status_code=status.HTTP_200_OK, response_model=ArticlesPaginatedResponseModel)
async def get_articles(page: int = Query(1), items_per_page: int = Query(20)):
    return articles_service.find_all(page=page, items_per_page=items_per_page)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ArticleResponse)
async def get_article_by_id(id: int = Path(...)):
    article = articles_service.find_by_id(id=id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
