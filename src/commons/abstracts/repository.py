import abc
from typing import Generic, Optional, Set, Type, TypeVar

T = TypeVar("T")


class AbstractRepository(abc.ABC, Generic[T]):
    seen: Set[T]
    not_found_exception: Type[Exception] = KeyError

    def add(self, obj: T):
        self._add(obj)
        self.seen.add(obj)

    def get(self, **kwargs) -> Optional[T]:
        obj = self._get(**kwargs)
        if obj:
            self.seen.add(obj)
        return obj

    @abc.abstractmethod
    def _add(self, obj: T):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, **kwargs) -> Optional[T]:
        raise NotImplementedError
