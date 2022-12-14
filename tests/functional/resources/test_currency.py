from unittest import mock

from src.adapters.repositories.apilayer_repository import (
    ApiLayerQuoted,
    ApiLayerRepository,
)
from src.domain.currency.models import Currency
from tests.conftest import CurrencyPriceEnumTest
from tests.factories.currency_factory import CurrencyFactory


def test_list_currencies_endpoint(uow, client):
    currency = CurrencyFactory.create(code="TEST")
    currency2 = CurrencyFactory.create(code="TEST2")
    with uow:
        uow.currencies.add(currency)
        uow.currencies.add(currency2)
        uow.commit()

    response = client.get("/api/v1/currencies/?limit=10")

    assert response.status_code == 200
    assert response.json()["total_count"] == 2


def test_create_currency_endpoint(uow, client):

    response = client.post("/api/v1/currencies/", json={"code": "TEST"})

    with uow:
        currency_db = uow.currencies.get(code="TEST")

    assert response.status_code == 201
    assert currency_db.code == "TEST"


def test_create_currency_endpoint_when_already_exists(uow, client):
    currency = CurrencyFactory.build(code="TEST")
    with uow:
        uow.currencies.add(currency)
        uow.commit()

    response = client.post("/api/v1/currencies/", json={"code": "TEST"})

    assert response.status_code == 409
    assert response.json()["detail"] == "CURRENCY_ALREADY_EXISTS"


def test_delete_currency_endpoint(uow, client):
    currency = CurrencyFactory.build(code="TEST")
    currency2 = CurrencyFactory.build(code="TEST2")
    currency3 = CurrencyFactory.build(code="TEST3")
    with uow:
        uow.currencies.add(currency)
        uow.currencies.add(currency2)
        uow.currencies.add(currency3)
        uow.commit()

        currency_db = uow.currencies.all()

    assert len(currency_db) == 3

    response = client.delete(f"/api/v1/currencies/{currency.id}")

    with uow:
        currency_db = uow.currencies.all()

    assert response.status_code == 204
    assert len(currency_db) == 2


def test_delete_currency_endpoint_when_not_found(uow, client):
    response = client.delete("/api/v1/currencies/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "CURRENCY_NOT_FOUND"


@mock.patch.object(
    ApiLayerRepository,
    "latest",
    return_value=[
        ApiLayerQuoted(code="USD", price=CurrencyPriceEnumTest.USD.value),
        ApiLayerQuoted(code="EUR", price=CurrencyPriceEnumTest.EUR.value),
        ApiLayerQuoted(code="INR", price=CurrencyPriceEnumTest.INR.value),
    ],
)
def test_convert_currency_endpoint(apilayer_repository, uow, client):
    brl = CurrencyFactory.create(code="BRL")
    eur = CurrencyFactory.create(code="EUR")
    inr = CurrencyFactory.create(code="INR")
    usd = CurrencyFactory.create(code="USD")
    with uow:
        uow.currencies.add(brl)
        uow.currencies.add(eur)
        uow.currencies.add(inr)
        uow.currencies.add(usd)
        uow.commit()

    response = client.get("/api/v1/currencies/convert/BRL/255.5")

    assert response.status_code == 200
    assert response.json() == {
        "USD": Currency("USD").total_price(255.5, CurrencyPriceEnumTest.USD.value),
        "EUR": Currency("EUR").total_price(255.5, CurrencyPriceEnumTest.EUR.value),
        "INR": Currency("INR").total_price(255.5, CurrencyPriceEnumTest.INR.value),
    }
