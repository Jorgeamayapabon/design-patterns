from structural_patterns.adapter.payment_processor import PaymentProcessor


class CheckoutService:
    def __init__(self, payment_processor: PaymentProcessor):
        self._payment_processor = payment_processor

    def checkout(self, amount: float):
        success = self._payment_processor.pay(amount, "COP")

        if not success:
            raise Exception("Pago fallido")

        print("Pago exitoso")
