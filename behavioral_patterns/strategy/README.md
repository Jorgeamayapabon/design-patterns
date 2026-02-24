# Patrón Strategy (Estrategia)

## Descripción

El **Strategy** es un patrón de diseño de comportamiento que define una familia de algoritmos, encapsula cada uno en una clase y los hace intercambiables. El patrón permite que el algoritmo varíe de forma independiente de los clientes que lo utilizan.

En lugar de tener condicionales o herencia para elegir un comportamiento, se delega la responsabilidad a objetos de estrategia que implementan una interfaz común. El contexto usa la estrategia actual sin conocer sus detalles concretos.

## Problema que resuelve

- Tienes varias formas de calcular algo (por ejemplo, coste de envío: estándar, express, internacional).
- Sin Strategy: muchos `if/elif` o subclases que solo cambian un método, lo que dificulta añadir nuevas variantes y mantener el código.
- Con Strategy: cada variante es una clase que implementa la misma interfaz; el contexto recibe la estrategia y la usa. Añadir una nueva estrategia es crear una nueva clase sin tocar el resto.

## Estructura del ejemplo

```
strategy/
├── shipping_strategy.py       # Interfaz de la estrategia (Strategy)
├── standard_shipping.py       # Estrategia concreta: envío estándar
├── express_shipping.py        # Estrategia concreta: envío express
├── international_shipping.py  # Estrategia concreta: envío internacional
├── shipping_context.py        # Contexto que usa la estrategia (ShippingCalculator)
├── main.py                    # Punto de entrada
├── README.md
└── TUTORIAL.md
```

## Componentes

| Rol | Clase/archivo | Descripción |
|-----|----------------|-------------|
| **Strategy** | `ShippingStrategy` | Interfaz común: `calculate(weight: float) -> float`. |
| **Concrete Strategy** | `StandardShipping`, `ExpressShipping`, `InternationalShipping` | Cada una implementa su fórmula de coste según el tipo de envío. |
| **Context** | `ShippingCalculator` | Recibe una estrategia en el constructor (o con `set_strategy`) y delega el cálculo en `calculate_cost(weight)`. |
| **Client** | `main.py` | Crea el contexto, asigna distintas estrategias y llama a `calculate_cost`. |

## Uso

Desde la raíz del proyecto:

```bash
python -m behavioral_patterns.strategy.main
```

El ejemplo calcula el coste de envío para un mismo peso usando envío estándar, express e internacional.

## Cuándo usarlo

- Tienes varias variantes de un mismo algoritmo y quieres poder cambiarlas en tiempo de ejecución.
- Quieres evitar condicionales complejos o herencia solo para cambiar un comportamiento.
- Quieres cumplir el principio Open/Closed: nuevas estrategias se añaden como nuevas clases sin modificar el contexto ni las estrategias existentes.

## Relación con otros patrones

- **State**: Similar en estructura (contexto + intercambiable), pero State cambia de comportamiento según estado interno; Strategy suele ser elegida externamente.
- **Template Method**: Define el esqueleto en una clase base; Strategy externaliza el algoritmo completo en objetos separados.
- **Decorator**: Añade responsabilidades envolviendo; Strategy reemplaza el algoritmo completo.

---

Para un recorrido paso a paso del ejemplo, consulta [TUTORIAL.md](./TUTORIAL.md).
