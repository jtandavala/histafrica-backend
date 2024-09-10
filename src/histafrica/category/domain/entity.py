import datetime
from typing import Optional
from dataclasses import dataclass, field
from histafrica.shared.domain.entity import Entity


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_activate: Optional[bool] = True
    created_at: Optional[datetime.datetime] = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    def __post_init__(self):
        if not self.created_at:
            self._set("created_at", datetime.datetime.now(datetime.timezone.utc))
        self.validate()

    def validate(self):
        pass
