import logging

from src.application.uow import SqlAlchemyUnitOfWork
from src.domain.currency.models import Currency

LOGGER = logging.getLogger(__name__)


def list_currencies(uow: SqlAlchemyUnitOfWork, limit: int) -> list[Currency]:
    with uow:
        return uow.currencies.all()[:limit]
