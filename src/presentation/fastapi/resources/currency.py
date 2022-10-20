from fastapi.routing import APIRouter
from pydantic.tools import parse_obj_as

from src.application.query_handlers.currency_query_handler import list_currencies
from src.application.uow import SqlAlchemyUnitOfWork
from src.presentation.fastapi.schemas.currency import CurrencySchema
from src.presentation.fastapi.schemas.pagination import Pagination

currency_router = APIRouter()


@currency_router.get(
    "/currencies", response_model=Pagination[CurrencySchema], tags=["v1/app"]
)
def get_currencies(limit: int = 10):
    uow = SqlAlchemyUnitOfWork()

    currencies = list_currencies(uow=uow, limit=limit)

    return Pagination[CurrencySchema](
        total_count=len(currencies),
        items=parse_obj_as(list[CurrencySchema], currencies),
    )
