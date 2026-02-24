from behavioral_patterns.strategy.shipping_strategy import ShippingStrategy


class ExpressShipping(ShippingStrategy):

    def calculate(self, weight: float) -> float:
        base_rate = 10.0
        return base_rate + (weight * 2.0)
