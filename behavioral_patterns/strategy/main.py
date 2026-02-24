from behavioral_patterns.strategy.express_shipping import ExpressShipping
from behavioral_patterns.strategy.international_shipping import InternationalShipping
from behavioral_patterns.strategy.shipping_context import ShippingCalculator
from behavioral_patterns.strategy.standard_shipping import StandardShipping


def run():
    weight = 5  # kg

    calculator = ShippingCalculator(StandardShipping())
    print("Standard:", calculator.calculate_cost(weight))

    calculator.set_strategy(ExpressShipping())
    print("Express:", calculator.calculate_cost(weight))

    calculator.set_strategy(InternationalShipping())
    print("International:", calculator.calculate_cost(weight))


if __name__ == "__main__":
    run()
