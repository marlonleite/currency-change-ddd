from src.application.query_handlers.currency_query_handler import list_currencies
from tests.factories.currency_factory import CurrencyFactory


def test_list_currencies(uow):
    brl = CurrencyFactory.create(code="BRL")
    usd = CurrencyFactory.create(code="USD")
    with uow:
        uow.currencies.add(brl)
        uow.currencies.add(usd)
        uow.commit()

    result = list_currencies(uow, 10)

    assert len(result) == 2
