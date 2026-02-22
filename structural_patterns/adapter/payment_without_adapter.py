from structural_patterns.adapter.payment_processor import PaymentProcessor


class PaymentWithoutAdapter(PaymentProcessor):
    def pay(self, amount: float, currency: str) -> bool:
        print(f"Pago sin adaptador... Total: {amount}, Moneda: {currency}")
        return True
