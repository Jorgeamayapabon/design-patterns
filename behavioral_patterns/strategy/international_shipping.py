from behavioral_patterns.strategy.shipping_strategy import ShippingStrategy


class InternationalShipping(ShippingStrategy):

    def calculate(self, weight: float) -> float:
        base_rate = 20.0
        customs_fee = 15.0
        return base_rate + customs_fee + (weight * 3.0)
