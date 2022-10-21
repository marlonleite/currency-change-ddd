from __future__ import annotations

from src.adapters.databases import Session
from src.adapters.repositories.currency_repository import CurrencyRepository
from src.commons.abstracts.unity_of_work import UnitOfWorkBase
from src.domain.currency.models import Currency

DEFAULT_SESSION_FACTORY = Session


class SqlAlchemyUnitOfWork(UnitOfWorkBase):
    currencies: CurrencyRepository
    default_session_factory = DEFAULT_SESSION_FACTORY

    def __init__(self, session_factory=None):
        self.session_factory = (
            session_factory
            if session_factory is not None
            else self.default_session_factory
        )

    def __enter__(self):
        self.session = self.session_factory()

        self.currencies = CurrencyRepository(self.session, Currency)

    def __exit__(self, type, *_):
        if type is not None:
            self.rollback()
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
