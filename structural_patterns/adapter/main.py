from structural_patterns.adapter.checkout_service import CheckoutService
from structural_patterns.adapter.external_payment_adapter import ExternalPaymentAdapter
from structural_patterns.adapter.external_payment_sdk import ExternalPaymentSDK
from structural_patterns.adapter.payment_without_adapter import PaymentWithoutAdapter


def run():
    sdk = ExternalPaymentSDK()
    adapter = ExternalPaymentAdapter(sdk)

    service = CheckoutService(adapter)
    service.checkout(100.50)

    # without adapter
    payment_processor = PaymentWithoutAdapter()
    service_without_adapter = CheckoutService(payment_processor)
    service_without_adapter.checkout(200.95)


if __name__ == "__main__":
    run()
