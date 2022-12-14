from enum import Enum

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import clear_mappers, scoped_session, sessionmaker

from src.adapters.databases import DB_ENGINE, mapper_registry
from src.adapters.orm import start_mappers
from src.adapters.repositories.apilayer_repository import ApiLayerRepository
from src.application.uow import SqlAlchemyUnitOfWork
from src.entrypoints.rest_application import get_app


@pytest.fixture(scope="session")
def engine():
    return DB_ENGINE


def create_db(engine):
    mapper_registry.metadata.create_all(engine)
    start_mappers()


def drop_db(engine):
    clear_mappers()
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def app():
    """An application for running tests"""
    yield get_app()


@pytest.fixture()
def client(app):
    yield TestClient(app)


@pytest.fixture()
def db_session(engine):
    drop_db(engine)
    create_db(engine)

    """
    Returns an sqlalchemy session, and after the test tears
    down everything properly.
    """
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = scoped_session(
        sessionmaker(
            bind=connection,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )
    )

    yield session

    session.close()

    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture()
def uow(db_session):
    yield SqlAlchemyUnitOfWork()


@pytest.fixture
def apilayer_repository(requests_mock, rates, latest_success):
    requests_mock.get(
        "http://test.com",
        json={},
    )
    requests_mock.get(
        "http://test.com/latest",
        json={
            "base": "BRL",
            "date": "2022-10-21",
            "rates": rates,
            "success": latest_success,
            "timestamp": 1666390863,
        },
    )
    yield ApiLayerRepository("http://test.com")


class CurrencyPriceEnumTest(Enum):
    EUR = 0.196411
    INR = 15.987327
    USD = 0.193689
