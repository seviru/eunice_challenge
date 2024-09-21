from typing import Callable

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from logger import logger

api = FastAPI()

from app.articles.entrypoint.rest import articles_router
api.include_router(articles_router)


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"errors": exc.errors(), "body": exc.body, "query_params": request.query_params}),
    )


@api.middleware("http")
async def logging_middleware(request: Request, call_next: Callable) -> Response:
    try:
        response: Response = await call_next(request)
    except Exception as e:
        logger.error(
            f"Server error occurred.",
            extra=dict(
                url=str(request.url),
                method=request.method,
                exception=e,
            ),
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "Internal server error", "details": str(e)},
        )

    if "/api/health" not in str(request.url):
        logger.info(
            f"URL: {request.url} | Status code {response.status_code}",
            extra={"method": request.method, "status_code": response.status_code},
        )

    return response
