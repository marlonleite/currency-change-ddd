from http import HTTPStatus

from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic.tools import parse_obj_as

from src.adapters.repositories.apilayer_repository import (
    ApiLayerRepository,
    ApiLayerResponseError,
)
from src.application.command_handlers.currency_command_handler import (
    convert_currency,
    create_currency,
    delete_currency,
)
from src.application.query_handlers.currency_query_handler import list_currencies
from src.application.uow import SqlAlchemyUnitOfWork
from src.domain.currency.commands import (
    ConvertCurrencyCommand,
    CreateCurrencyCommand,
    DeleteCurrencyCommand,
)
from src.domain.currency.exceptions import CurrencyAlreadyExists, CurrencyNotFound
from src.presentation.fastapi.schemas.currency import (
    CreateCurrencySchema,
    CurrencySchema,
)
from src.presentation.fastapi.schemas.pagination import Pagination

currency_router = APIRouter()


@currency_router.get(
    "/currencies",
    response_model=Pagination[CurrencySchema],
    tags=["v1/app"],
)
def get_currencies(limit: int = 10):
    uow = SqlAlchemyUnitOfWork()

    currencies = list_currencies(uow=uow, limit=limit)

    return Pagination[CurrencySchema](
        total_count=len(currencies),
        items=parse_obj_as(list[CurrencySchema], currencies),
    )


@currency_router.post(
    "/currencies",
    response_model=CurrencySchema,
    status_code=HTTPStatus.CREATED,
    tags=["v1/app"],
)
def create_currencies(data: CreateCurrencySchema):
    try:
        command = CreateCurrencyCommand(code=data.code)
        uow = SqlAlchemyUnitOfWork()
        currency = create_currency(command, uow)
        return parse_obj_as(CurrencySchema, currency)
    except CurrencyAlreadyExists as exc:
        raise HTTPException(HTTPStatus.CONFLICT, detail=exc.public_message) from exc


@currency_router.delete(
    "/currencies/{item_id}",
    status_code=HTTPStatus.NO_CONTENT,
    tags=["v1/app"],
)
def delete_currencies(item_id: int):
    try:
        uow = SqlAlchemyUnitOfWork()
        command = DeleteCurrencyCommand(item_id=item_id)
        delete_currency(command, uow)
        return Response(status_code=HTTPStatus.NO_CONTENT)
    except CurrencyNotFound as exc:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=exc.public_message) from exc


@currency_router.get(
    "/convert/{code}/{amount}",
    tags=["v1/app"],
)
async def convert(code: str, amount: float):
    try:
        command = ConvertCurrencyCommand(
            code=code,
            amount=amount,
        )
        uow = SqlAlchemyUnitOfWork()
        apilayer_repository = ApiLayerRepository()
        result = convert_currency(
            command=command, uow=uow, apilayer_repository=apilayer_repository
        )
        return JSONResponse(content=result)
    except ApiLayerResponseError as exc:
        raise HTTPException(HTTPStatus.CONFLICT, detail=exc.public_message) from exc
