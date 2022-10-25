import logging

from src.adapters.repositories.apilayer_repository import (
    ApiLayerRepository,
    ApiLayerResponseError,
)
from src.application.uow import SqlAlchemyUnitOfWork
from src.domain.currency.commands import ConvertCurrencyCommand, CreateCurrencyCommand
from src.domain.currency.exceptions import (
    CurrencyAlreadyExists,
    CurrencyConvertInconsistentError,
    CurrencyNotFound,
)
from src.domain.currency.models import Currency

LOGGER = logging.getLogger(__name__)


def create_currency(
    command: CreateCurrencyCommand, uow: SqlAlchemyUnitOfWork
) -> Currency:
    with uow:
        currency = uow.currencies.get(code=command.code)

        if currency is not None:
            LOGGER.warning(CurrencyAlreadyExists.message(currency.id))
            raise CurrencyAlreadyExists.create(currency.id)

        new_currency = Currency(code=command.code)

        uow.currencies.add(new_currency)
        uow.commit()

        return new_currency


def delete_currency(currency_id: int, uow: SqlAlchemyUnitOfWork) -> None:
    with uow:
        currency = uow.currencies.get(id=currency_id)

        if currency is None:
            LOGGER.warning(CurrencyNotFound.message(currency_id))
            raise CurrencyNotFound.create(currency_id)

        uow.currencies.delete(currency)
        uow.commit()


def convert_currency(
    command: ConvertCurrencyCommand,
    uow: SqlAlchemyUnitOfWork,
    apilayer_repository: ApiLayerRepository,
) -> dict:
    with uow:
        codes = [
            currency.code
            for currency in uow.currencies.all()
            if currency.code not in command.code
        ]

        try:
            latest = apilayer_repository.latest(base=command.code, symbols=codes)
        except ApiLayerResponseError as exc:
            LOGGER.warning(CurrencyConvertInconsistentError.message(command.code))
            raise CurrencyConvertInconsistentError.create(command.code) from exc

        items = {}
        for rate in latest:
            currency = Currency(code=rate.code)
            calculatiuon = currency.total_price(amount=command.amount, price=rate.price)
            items[currency.code] = calculatiuon

        return items
