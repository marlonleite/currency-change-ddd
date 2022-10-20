import logging

from sqlalchemy.orm import clear_mappers

from src.adapters.databases import mapper_registry
from src.adapters.models import currency_table
from src.domain.currency.models import Currency

LOGGER = logging.getLogger(__name__)


def start_mappers():
    clear_mappers()

    mapper_registry.map_imperatively(Currency, currency_table)
