from dataclasses import dataclass
from typing import Any, Dict, List

ErrorFields = Dict[str, List[str]]


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        return ValidatorRules(value, prop)
