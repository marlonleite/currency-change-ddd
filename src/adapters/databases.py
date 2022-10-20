from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session as SessionModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import registry

from src.commons.config import settings

DRIVER_REGISTER_ENGINE: Engine = create_engine(settings.DATABASE_URI)

Session: Callable[..., SessionModel] = sessionmaker(
    bind=DRIVER_REGISTER_ENGINE,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

mapper_registry = registry()
