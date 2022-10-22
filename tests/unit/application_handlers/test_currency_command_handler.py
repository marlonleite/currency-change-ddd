import pytest

from src.application.command_handlers.currency_command_handler import (
    convert_currency,
    create_currency,
    delete_currency,
)
from src.domain.currency.commands import ConvertCurrencyCommand, CreateCurrencyCommand
from src.domain.currency.exceptions import (
    CurrencyAlreadyExists,
    CurrencyConvertInconsistentError,
    CurrencyNotFound,
)
from src.domain.currency.models import Currency
from tests.conftest import CurrencyPriceEnumTest
from tests.factories.currency_factory import CurrencyFactory


def test_create_currency(uow):
    create_currency_command = CreateCurrencyCommand(code="Test")
    create_currency(command=create_currency_command, uow=uow)

    with uow:
        currency_from_db = uow.currencies.get(code="Test")

    assert currency_from_db.code == "Test"


def test_create_currency_when_fails(uow):
    currency = CurrencyFactory.build(code="Test")
    with uow:
        uow.currencies.add(currency)
        uow.commit()

    with pytest.raises(CurrencyAlreadyExists) as exc_info:
        create_currency_command = CreateCurrencyCommand(code="Test")
        create_currency(command=create_currency_command, uow=uow)

    assert str(exc_info.value) == f"Currency already exists: currency_id={currency.id}"


def test_delete_currency(uow):
    currency = CurrencyFactory.build(code="Test")
    with uow:
        uow.currencies.add(currency)
        uow.commit()

    delete_currency(currency_id=currency.id, uow=uow)

    with uow:
        currency_from_db = uow.currencies.get(id=currency.id)

    assert currency_from_db is None


def test_delete_currency_fail(uow):
    with pytest.raises(CurrencyNotFound) as exc_info:
        delete_currency(currency_id=1, uow=uow)

    assert str(exc_info.value) == "Currency not found: currency_id=1"


@pytest.mark.parametrize(
    "rates",
    [
        {
            "EUR": CurrencyPriceEnumTest.EUR.value,
            "INR": CurrencyPriceEnumTest.INR.value,
            "USD": CurrencyPriceEnumTest.USD.value,
        },
    ],
)
@pytest.mark.parametrize("latest_success", [True])
def test_convert_currency(uow, apilayer_repository):
    brl = CurrencyFactory.build(code="BRL")
    usd = CurrencyFactory.build(code="USD")
    inr = CurrencyFactory.build(code="INR")
    eur = CurrencyFactory.build(code="EUR")
    with uow:
        uow.currencies.add(brl)
        uow.currencies.add(usd)
        uow.currencies.add(inr)
        uow.currencies.add(eur)
        uow.commit()

    command = ConvertCurrencyCommand(code="BRL", amount=159.5)
    result = convert_currency(
        command=command, uow=uow, apilayer_repository=apilayer_repository
    )

    assert isinstance(result, dict)
    assert result == {
        "EUR": Currency("EUR").total_price(159.5, CurrencyPriceEnumTest.EUR.value),
        "INR": Currency("INR").total_price(159.5, CurrencyPriceEnumTest.INR.value),
        "USD": Currency("USD").total_price(159.5, CurrencyPriceEnumTest.USD.value),
    }


@pytest.mark.parametrize(
    "rates",
    [
        {
            "EUR": CurrencyPriceEnumTest.EUR.value,
            "INR": CurrencyPriceEnumTest.INR.value,
            "USD": CurrencyPriceEnumTest.USD.value,
        },
    ],
)
@pytest.mark.parametrize("latest_success", [False])
def test_convert_currency_when_fails(uow, apilayer_repository):
    brl = CurrencyFactory.build(code="BRL")
    usd = CurrencyFactory.build(code="USD")
    inr = CurrencyFactory.build(code="INR")
    eur = CurrencyFactory.build(code="EUR")
    with uow:
        uow.currencies.add(brl)
        uow.currencies.add(usd)
        uow.currencies.add(inr)
        uow.currencies.add(eur)
        uow.commit()

    with pytest.raises(CurrencyConvertInconsistentError) as exc_info:
        command = ConvertCurrencyCommand(code="BRL", amount=159.5)
        convert_currency(
            command=command, uow=uow, apilayer_repository=apilayer_repository
        )

    assert str(exc_info.value) == "Currency not found: currency_code=BRL"
