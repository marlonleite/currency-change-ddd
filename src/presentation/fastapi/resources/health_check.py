from fastapi.routing import APIRouter

from src.presentation.fastapi.schemas.health_check import Message

health_router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
)


@health_router.get("/")
def health_check():
    return Message(message="Ok")
