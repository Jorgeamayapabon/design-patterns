from abc import ABC, abstractmethod


class IBuilderHttpRequest(ABC):
    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def set_url(self, url: str) -> None:
        pass

    @abstractmethod
    def set_method(self, method: str) -> None:
        pass

    @abstractmethod
    def set_body(self, body: dict) -> None:
        pass

    @abstractmethod
    def set_timeout(self, timeout: int) -> None:
        pass
    
    @abstractmethod
    def add_header(self, key: str, value: str) -> None:
        pass
