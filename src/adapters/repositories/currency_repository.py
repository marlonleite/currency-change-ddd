from src.adapters.sqlalchemy_repository import CRUDSqlAlchemyRepository
from src.domain.currency.models import Currency


class CurrencyRepository(CRUDSqlAlchemyRepository[Currency]):
    pass
