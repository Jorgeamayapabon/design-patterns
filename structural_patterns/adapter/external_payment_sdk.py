class ExternalPaymentSDK:
    def make_transaction(self, total_in_cents: int, currency_code: str) -> dict:
        print(f"Procesando pago en proveedor externo... total: {total_in_cents}, moneda:{currency_code}")
        return {"status": "success"}
