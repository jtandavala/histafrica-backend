from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, List, TypeVar

from histafrica.shared.domain.entity import Entity
from histafrica.shared.domain.exceptions import NotFoundException
from histafrica.shared.domain.value_objects import UniqueEntityId

ET = TypeVar("ET", bound=Entity)


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
        pass

    def update(self, entity: ET) -> None:
        pass

    def delete(self, entoty: ET) -> None:
        pass

    def _get(self, entity_id: str) -> ET:
        entity = next(filter(lambda i: i.id == entity_id, self.items), None)

        if not entity:
            raise NotFoundException(f"Entity not found using ID '{entity_id}'")
        return entity
