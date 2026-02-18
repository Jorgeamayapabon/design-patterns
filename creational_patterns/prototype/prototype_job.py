from abc import ABC, abstractmethod
from typing import Any


class IPrototypeJob(ABC):

    @abstractmethod
    def clone(self) -> Any:
        pass
