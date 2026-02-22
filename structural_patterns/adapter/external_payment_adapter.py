from structural_patterns.adapter.external_payment_sdk import ExternalPaymentSDK
from structural_patterns.adapter.payment_processor import PaymentProcessor


class ExternalPaymentAdapter(PaymentProcessor):
    def __init__(self, external_sdk: ExternalPaymentSDK):
        self._external_sdk = external_sdk

    def pay(self, amount: float, currency: str) -> bool:
        # Adaptación de formato
        total_in_cents = int(amount * 100)

        response = self._external_sdk.make_transaction(
            total_in_cents=total_in_cents,
            currency_code=currency
        )

        # Adaptación de respuesta
        return response.get("status") == "success"
