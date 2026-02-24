# Tutorial: Patrón Strategy

Este tutorial recorre el ejemplo del calculador de costes de envío y muestra cómo el patrón Strategy permite intercambiar algoritmos (estándar, express, internacional) sin modificar el código del contexto.

## Objetivo

Hacer que un **ShippingCalculator** pueda calcular el coste de envío usando distintas fórmulas (estándar, express, internacional) de forma intercambiable, sin condicionales ni herencia de comportamiento.

## Paso 1: La interfaz de la estrategia (Strategy)

En `shipping_strategy.py` se define la interfaz que todas las estrategias deben implementar:

```python
class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, weight: float) -> float:
        pass
```

- Recibe el **peso** (float) del paquete.
- Devuelve el **coste** (float) según la lógica de esa estrategia.

Cualquier nueva forma de envío solo tiene que implementar esta interfaz.

## Paso 2: Estrategias concretas

Cada tipo de envío es una clase que implementa `ShippingStrategy`:

**StandardShipping** (`standard_shipping.py`): tarifa base + peso × 1.0  
**ExpressShipping** (`express_shipping.py`): tarifa base mayor + peso × 2.0  
**InternationalShipping** (`international_shipping.py`): tarifa base + aduanas + peso × 3.0  

Ejemplo de una estrategia concreta:

```python
class StandardShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        base_rate = 5.0
        return base_rate + (weight * 1.0)
```

El contexto no necesita conocer los detalles; solo llama a `calculate(weight)`.

## Paso 3: El contexto (ShippingCalculator)

En `shipping_context.py`, el contexto recibe una estrategia y delega en ella:

```python
class ShippingCalculator:
    def __init__(self, strategy: ShippingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ShippingStrategy):
        self._strategy = strategy

    def calculate_cost(self, weight: float) -> float:
        return self._strategy.calculate(weight)
```

- En el constructor se puede fijar la estrategia inicial.
- `set_strategy` permite **cambiar de estrategia en tiempo de ejecución**.
- `calculate_cost` solo delega en la estrategia actual; no contiene condicionales ni fórmulas.

## Paso 4: El cliente (main)

En `main.py` se ensambla el contexto y se prueban las tres estrategias:

```python
weight = 5  # kg

calculator = ShippingCalculator(StandardShipping())
print("Standard:", calculator.calculate_cost(weight))

calculator.set_strategy(ExpressShipping())
print("Express:", calculator.calculate_cost(weight))

calculator.set_strategy(InternationalShipping())
print("International:", calculator.calculate_cost(weight))
```

El mismo objeto `calculator` calcula con estándar, luego se le asigna express y después internacional, sin crear nuevos contextos.

## Paso 5: Ejecutar el ejemplo

Desde la raíz del proyecto:

```bash
python -m behavioral_patterns.strategy.main
```

Deberías ver tres líneas con el coste para el mismo peso según cada estrategia.

## Resumen del flujo

1. **Cliente** crea un `ShippingCalculator` con una estrategia (por ejemplo `StandardShipping`).
2. **Cliente** llama `calculator.calculate_cost(weight)`.
3. **ShippingCalculator** delega en `self._strategy.calculate(weight)`.
4. La **estrategia concreta** aplica su fórmula y devuelve el coste.
5. Si el cliente llama `set_strategy(ExpressShipping())`, los siguientes `calculate_cost` usarán la fórmula express.

Con esto tienes un ejemplo completo del patrón Strategy aplicado al cálculo de envíos. Para más contexto y cuándo usarlo, revisa el [README.md](./README.md) del patrón.
