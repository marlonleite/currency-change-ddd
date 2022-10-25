import logging
from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

LOGGER = logging.getLogger(__name__)


class LoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs all requests
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        LOGGER.info(f'{request.method} on path {request.scope["path"]}')
        return await call_next(request)
