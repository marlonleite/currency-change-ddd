import factory

from src.domain.currency.models import Currency


class CurrencyFactory(factory.Factory):
    class Meta:
        model = Currency

    code = factory.Faker("name")
