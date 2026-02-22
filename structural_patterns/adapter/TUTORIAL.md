# Tutorial: Patrón Adapter

Este tutorial recorre el ejemplo de pago con un SDK externo y muestra cómo el Adapter permite usarlo sin cambiar la interfaz que espera tu aplicación.

## Objetivo

Hacer que un **CheckoutService** que trabaja con `PaymentProcessor.pay(amount, currency)` pueda usar un SDK externo que solo tiene `make_transaction(total_in_cents, currency_code)`.

## Paso 1: La interfaz que espera el cliente (Target)

En `payment_processor.py` se define la interfaz que usa todo el código de checkout:

```python
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float, currency: str) -> bool:
        pass
```

- Recibe **monto en unidades** (float) y **moneda** (str).
- Devuelve un **bool** indicando éxito o fallo.

El cliente (`CheckoutService`) depende solo de esta abstracción.

## Paso 2: El SDK externo (Adaptee)

En `external_payment_sdk.py` está la API de terceros:

```python
class ExternalPaymentSDK:
    def make_transaction(self, total_in_cents: int, currency_code: str) -> dict:
        # ...
        return {"status": "success"}
```

- Espera **monto en centavos** (int) y **código de moneda** (str).
- Devuelve un **dict** con `"status"`, no un bool.

Aquí está la incompatibilidad: nombres, tipos y formatos distintos.

## Paso 3: El adaptador

En `external_payment_adapter.py`, el adaptador:

1. **Implementa** la interfaz que espera el cliente (`PaymentProcessor`).
2. **Envuelve** una instancia del SDK (`ExternalPaymentSDK`).
3. **Traduce** en `pay()`:
   - `amount` (float) → `total_in_cents` (int) multiplicando por 100.
   - `currency` → `currency_code`.
   - Respuesta `dict` → `True` si `status == "success"`, sino `False`.

Así el cliente sigue llamando `pay(amount, currency)` y el adaptador se encarga de hablar con el SDK.

## Paso 4: El cliente (CheckoutService)

En `checkout_service.py`, el servicio recibe cualquier `PaymentProcessor`:

```python
class CheckoutService:
    def __init__(self, payment_processor: PaymentProcessor):
        self._payment_processor = payment_processor

    def checkout(self, amount: float):
        success = self._payment_processor.pay(amount, "COP")
        # ...
```

No importa si por detrás es un adaptador al SDK externo o una implementación propia; el código del checkout no cambia.

## Paso 5: Ensamblar y ejecutar

En `main.py` se muestra el uso con y sin adaptador:

```python
# Con adaptador: CheckoutService usa el SDK externo a través del adaptador
sdk = ExternalPaymentSDK()
adapter = ExternalPaymentAdapter(sdk)
service = CheckoutService(adapter)
service.checkout(100.50)

# Sin adaptador: implementación que ya cumple PaymentProcessor
payment_processor = PaymentWithoutAdapter()
service_without_adapter = CheckoutService(payment_processor)
service_without_adapter.checkout(200.95)
```

Ejecuta desde la raíz del proyecto:

```bash
python -m structural_patterns.adapter.main
```

## Resumen del flujo

1. **CheckoutService** llama `pay(100.50, "COP")` sobre el objeto que recibe (aquí, el adaptador).
2. **ExternalPaymentAdapter** convierte a `total_in_cents=10050`, `currency_code="COP"` y llama al SDK.
3. **ExternalPaymentSDK** devuelve `{"status": "success"}`.
4. El adaptador convierte eso en `True` y lo devuelve a **CheckoutService**.

Con esto tienes un ejemplo completo del patrón Adapter aplicado a un procesador de pagos. Para más contexto y cuándo usarlo, revisa el [README.md](./README.md) del patrón.
