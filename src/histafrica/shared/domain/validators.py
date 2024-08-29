from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar

from .exceptions import ValidationException

ErrorFields = Dict[str, List[str]]
PropsValidated = TypeVar("PropsValidated")


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        return ValidatorRules(value, prop)

    def required(self) -> "ValidatorRules":
        if self.value is None or self.value == "":
            raise ValidationException(f"The {self.prop} is required")
        return self

    def string(self) -> "ValidatorRules":
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f"The {self.prop} must be a string")
        return self

    def max_length(self, max_length: int) -> "ValidatorRules":
        if self.value is not None and len(self.value) > max_length:
            raise ValidationException(
                f"The {self.prop} must be less than {max_length} characters"
            )
        return self

    def boolean(self) -> "ValidatorRules":
        if self.value is not None and not isinstance(self.value, bool):
            raise ValidationException(f"The {self.prop} must be a boolean")
        return self


@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):
    errors: ErrorFields = None
    validated_data: PropsValidated = None

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()
