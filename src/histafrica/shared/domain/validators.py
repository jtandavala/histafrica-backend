from dataclasses import dataclass
from typing import Any, Dict, List

from .exceptions import ValidationException

ErrorFields = Dict[str, List[str]]


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        return ValidatorRules(value, prop)

    def required(self) -> "ValidatorRules":
        if self.value is None or self.value == "":
            raise ValidationException(f"The {self.prop} must be a string")
        return self
