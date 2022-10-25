from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class Pagination(GenericModel, Generic[T]):
    items: list[T]
    page: int = 1
    per_page: int = 10
    total_count: int
    next: str | None
    previous: str | None
