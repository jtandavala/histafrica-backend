from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class UseCase(Generic[Input, Output], ABC):

    @abstractmethod
    def execute(self, input_dto: Input) -> Output:
        raise NotImplementedError()
