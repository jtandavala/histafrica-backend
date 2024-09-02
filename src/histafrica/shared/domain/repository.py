from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, TypeVar

from histafrica.shared.domain.entity import Entity
from histafrica.shared.domain.exceptions import NotFoundException
from histafrica.shared.domain.value_objects import UniqueEntityId

ET = TypeVar("ET", bound=Entity)
Filter = TypeVar("Filter", str, Any)
Input = TypeVar("Input")
Output = TypeVar("OutPut")


class RepositoryInterface(Generic[ET], ABC):

    @abstractmethod
    def insert(self, entity: ET) -> None:
        raise NotImplementedError()

    def bulk_insert(self, entities: List[ET]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> List[ET]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: ET) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity_id: str | UniqueEntityId) -> None:
        raise NotImplementedError()


@dataclass(slots=True)
class InMemoryRepository(RepositoryInterface[ET], ABC):
    items: List[ET] = field(default_factory=lambda: [])

    def insert(self, entity: ET) -> None:
        self.items.append(entity)

    def bulk_insert(self, entities: List[ET]) -> None:
        pass

    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        return self._get(str(entity_id))

    def find_all(self) -> List[ET]:
        return self.items

    def update(self, entity: ET) -> None:
        entity_found = self._get(entity.id)
        index = self.items.index(entity_found)
        self.items[index] = entity

    def delete(self, entity: ET) -> None:
        entity_found = self._get(entity.id)
        self.items.remove(entity_found)

    def _get(self, entity_id: str) -> ET:
        entity = next(filter(lambda i: i.id == entity_id, self.items), None)

        if not entity:
            raise NotFoundException(f"Entity not found using ID '{entity_id}'")
        return entity


class SearchableRepositoryInterface(
    Generic[ET, Input, Output], RepositoryInterface[ET], ABC
):
    sortable_fields: List[str] = []

    @abstractmethod
    def search(self, input_params: Input) -> Output:
        raise NotImplementedError()


@dataclass(slots=True, kw_only=True)
class SearchParams(Generic[Filter]):
    page: Optional[int] = 1
    per_page: Optional[int] = 15
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None

    def __post_init__(self):
        self._normalize_page()
        self._normalize_per_page()
        self._normalize_sort()
        self._normalize_sort_dir()
        self._normalize_filter()

    def _normalize_page(self):
        page = self._convert_to_int(self.page)
        if page <= 0:
            page = self._get_dataclass_field("page").default
        self.page = page

    def _normalize_per_page(self):
        per_page = self._convert_to_int(self.per_page)
        if per_page < 1:
            per_page = self._get_dataclass_field("per_page").default
        self.per_page = per_page

    def _normalize_sort(self):
        self.sort = None if self.sort == "" or self.sort is None else str(self.sort)

    def _normalize_sort_dir(self):
        if not self.sort:
            self.sort_dir = None
            return
        sort_dir = str(self.sort_dir).lower()
        self.sort_dir = "asc" if sort_dir not in ["asc", "desc"] else sort_dir

    def _normalize_filter(self):
        self.filter = (
            None if self.filter == "" or self.filter is None else str(self.filter)
        )

    def _convert_to_int(self, value: Any, default=0) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def _get_dataclass_field(self, field_name):
        return SearchParams.__dataclass_fields__[field_name]
