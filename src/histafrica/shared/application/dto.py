from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

Filter = TypeVar("Filter")


@dataclass(frozen=True, slots=True)
class SearchInput(Generic[Filter]):
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None


Item = TypeVar("Item")


@dataclass(frozen=True, slots=True)
class PaginationOutput(Generic[Item]):
    items: List[Item]
    total: int
    current_page: int
    per_page: int
    last_page: int
