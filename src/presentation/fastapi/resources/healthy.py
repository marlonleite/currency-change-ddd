from fastapi.routing import APIRouter

from src.presentation.fastapi.schemas.healthy import Message

health_router = APIRouter()


@health_router.get(
    "/health",
)
def healthy():
    return Message(message="Ok")
