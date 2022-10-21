from typing import List, Optional, Type, TypeVar

from sqlalchemy.orm.session import Session

from src.commons.abstracts.repository import AbstractRepository

T = TypeVar("T")


class CRUDSqlAlchemyRepository(AbstractRepository[T]):
    def __init__(self, session: Session, obj_type: Type[T]):
        self.session = session
        self.obj_type = obj_type
        self.seen = set()

    def _add(self, obj: T):
        self.session.add(obj)

    def _get(self, **kwargs) -> Optional[T]:
        return self.session.query(self.obj_type).filter_by(**kwargs).first()

    def _delete(self, obj: T):
        self.session.delete(obj)

    def all(self) -> List[T]:
        return self.session.query(self.obj_type).all()

    def filter(self, **kwargs) -> List[T]:
        return self.session.query(self.obj_type).filter_by(**kwargs).all()
