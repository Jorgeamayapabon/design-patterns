# Patrón Adapter (Adaptador)

## Descripción

El **Adapter** es un patrón estructural que permite que objetos con interfaces incompatibles trabajen juntos. Actúa como un puente entre una interfaz que tu código espera y otra que proporciona una clase o librería externa, sin modificar el código existente ni el código de terceros.

## Problema que resuelve

- Tu aplicación usa una interfaz `PaymentProcessor` con el método `pay(amount: float, currency: str) -> bool`.
- Un SDK externo ofrece `make_transaction(total_in_cents: int, currency_code: str) -> dict`.
- Sin adaptador tendrías que cambiar todo el código que usa `PaymentProcessor` o modificar el SDK (si fuera posible).

El adaptador traduce llamadas entre ambas interfaces y adapta formatos (por ejemplo, monto en decimal a centavos, respuesta `dict` a `bool`).

## Estructura del ejemplo

```
adapter/
├── payment_processor.py      # Interfaz que espera el cliente (target)
├── external_payment_sdk.py   # API externa con interfaz distinta (adaptee)
├── external_payment_adapter.py  # Adaptador que implementa PaymentProcessor y delega al SDK
├── checkout_service.py       # Cliente que depende de PaymentProcessor
├── payment_without_adapter.py   # Implementación “nativa” para comparación
├── main.py                   # Punto de entrada
├── README.md
└── TUTORIAL.md
```

## Componentes

| Rol | Clase/archivo | Descripción |
|-----|----------------|-------------|
| **Target** | `PaymentProcessor` | Interfaz que usa el cliente (`pay(amount, currency) -> bool`). |
| **Adaptee** | `ExternalPaymentSDK` | API externa con `make_transaction(total_in_cents, currency_code) -> dict`. |
| **Adapter** | `ExternalPaymentAdapter` | Implementa `PaymentProcessor`, envuelve el SDK y traduce parámetros y respuesta. |
| **Client** | `CheckoutService` | Recibe un `PaymentProcessor` y llama a `pay()`; no conoce el SDK. |

## Uso

Desde la raíz del proyecto:

```bash
python -m structural_patterns.adapter.main
```

El ejemplo ejecuta el checkout con el adaptador (usando el SDK externo) y también con una implementación sin adaptador para comparar.

## Cuándo usarlo

- Integrar librerías o APIs de terceros cuya interfaz no coincide con la de tu aplicación.
- Reutilizar código legacy que tiene una interfaz distinta a la que esperan los nuevos módulos.
- Quieres mantener el principio de inversión de dependencias: el cliente depende de una abstracción (`PaymentProcessor`), no del SDK concreto.

## Relación con otros patrones

- **Decorator**: Añade responsabilidades; el Adapter cambia la interfaz.
- **Facade**: Simplifica una interfaz compleja; el Adapter traduce entre dos interfaces concretas.
- **Proxy**: Misma interfaz que el sujeto; el Adapter ofrece una interfaz distinta al adaptee.

---

Para un recorrido paso a paso del ejemplo, consulta [TUTORIAL.md](./TUTORIAL.md).
