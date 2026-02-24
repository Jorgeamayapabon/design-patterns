from behavioral_patterns.strategy.shipping_strategy import ShippingStrategy


class ShippingCalculator:

    def __init__(self, strategy: ShippingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ShippingStrategy):
        self._strategy = strategy

    def calculate_cost(self, weight: float) -> float:
        return self._strategy.calculate(weight)
