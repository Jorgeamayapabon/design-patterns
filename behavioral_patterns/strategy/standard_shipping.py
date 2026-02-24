from behavioral_patterns.strategy.shipping_strategy import ShippingStrategy


class StandardShipping(ShippingStrategy):

    def calculate(self, weight: float) -> float:
        base_rate = 5.0
        return base_rate + (weight * 1.0)
