import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.orm import start_mappers
from src.commons.config import settings
from src.commons.middleware.logger_middleware import LoggerMiddleware
from src.presentation.fastapi.v1 import router as v1_router

LOGGER = logging.getLogger(__name__)


def get_app() -> FastAPI:
    app = FastAPI(
        title=settings.REST_APPLICATION_NAME,
        description=settings.REST_APPLICATION_DESCRIPTION,
        openapi_url="/api/openapi.json",
    )
    app.add_middleware(LoggerMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.APPLICATION_URL_CORS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    start_mappers()

    app.include_router(v1_router)

    return app


if __name__ == "__main__":
    import uvicorn

    LOGGER.info("Starting application ..")
    uvicorn.run(
        "rest_application:get_app",
        workers=settings.REST_APPLICATION_WORKERS,
        host=settings.REST_APPLICATION_HOST,
        port=settings.REST_APPLICATION_PORT,
        reload=settings.REST_APPLICATION_RELOAD,
        factory=True,
    )
