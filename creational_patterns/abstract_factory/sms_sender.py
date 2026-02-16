from abc import ABC, abstractmethod


class ISmsSender(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> None:
        pass
