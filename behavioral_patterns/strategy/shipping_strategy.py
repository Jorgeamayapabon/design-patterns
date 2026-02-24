from abc import ABC, abstractmethod


class ShippingStrategy(ABC):

    @abstractmethod
    def calculate(self, weight: float) -> float:
        pass
