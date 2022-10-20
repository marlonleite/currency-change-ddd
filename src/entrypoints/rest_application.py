import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.commons.config import settings
from src.commons.middleware.logger_middleware import LoggerMiddleware

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
