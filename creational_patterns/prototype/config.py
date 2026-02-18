from creational_patterns.prototype.prototype_job import IPrototypeJob
from typing import Any, Dict
import copy

class JobConfig(IPrototypeJob):
    def __init__(
        self, 
        name: str, 
        retries: int, 
        timeout: int, 
        metadata: Dict[str, Any]
    ):
        self._name = name
        self._retries = retries
        self._timeout = timeout
        self.metadata = metadata

    def clone(self) -> "JobConfig":
        return copy.deepcopy(self)

    def __repr__(self):
        return (
            f"JobConfig(name={self._name!r}, "
            f"retries={self._retries!r}, "
            f"timeout={self._timeout!r}, "
            f"metadata={self.metadata!r})"
        )
