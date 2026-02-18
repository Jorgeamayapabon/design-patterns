# Patrón Builder (Constructor)

## Descripción

El patrón **Builder** es un patrón de diseño creacional que permite construir objetos complejos paso a paso. A diferencia de otros patrones creacionales que construyen productos en un solo paso, el Builder permite producir distintos tipos y representaciones de un objeto usando el mismo código de construcción.

## Propósito

- Separar la construcción de un objeto complejo de su representación
- Permitir la misma construcción para crear diferentes representaciones
- Construir objetos paso a paso con control total sobre el proceso
- Evitar constructores con múltiples parámetros (telescoping constructor anti-pattern)

## Implementación en este Proyecto

Este ejemplo implementa un **Constructor de Peticiones HTTP** que permite crear objetos `HttpRequest` de manera flexible y controlada, con múltiples configuraciones como GET, POST, PUT, con diferentes headers, body, timeout, etc.

### Estructura del Proyecto

```
builder/
├── http_request.py                      # Producto final (HttpRequest)
├── builder_http_request.py              # Interfaz del Builder
├── builder_concrete_http_request.py     # Builder concreto
├── builder_director.py                  # Director (opcional)
└── main.py                              # Ejemplos de uso
```

### Componentes Principales

#### 1. Producto
- **`HttpRequest`**: La clase compleja que queremos construir
  - URL
  - Método HTTP (GET, POST, PUT, etc.)
  - Headers
  - Body
  - Timeout

#### 2. Interfaz Builder
- **`IBuilderHttpRequest`**: Define los pasos para construir un HttpRequest
  - `reset()` - Reinicia el builder
  - `set_url()` - Establece la URL
  - `set_method()` - Establece el método HTTP
  - `set_body()` - Establece el cuerpo de la petición
  - `set_timeout()` - Establece el timeout
  - `add_header()` - Agrega un header

#### 3. Builder Concreto
- **`BuilderConcreteHttpRequest`**: Implementa la interfaz del builder y construye el objeto paso a paso

#### 4. Director (Opcional)
- **`BuilderDirector`**: Encapsula las recetas para construir configuraciones específicas de peticiones HTTP (GET, POST, PUT)

## Ventajas

- **Construcción Paso a Paso**: Construye objetos complejos de forma incremental
- **Código Reutilizable**: El mismo proceso de construcción para diferentes representaciones
- **Aislamiento**: El código de construcción está separado de la lógica de negocio
- **Control Fino**: Control total sobre cada paso del proceso de construcción
- **Legibilidad**: Código más legible que constructores con múltiples parámetros
- **Principio de Responsabilidad Única**: La construcción está separada de la representación

## Uso Básico

### Opción 1: Usando el Director

```python
from creational_patterns.builder.builder_concrete_http_request import BuilderConcreteHttpRequest
from creational_patterns.builder.builder_director import BuilderDirector

# Crear builder y director
builder = BuilderConcreteHttpRequest()
director = BuilderDirector(builder)

# Construir una petición GET usando el director
director.build_get_request()
get_request = builder.get_request()
print(get_request)

# Construir una petición POST usando el director
director.build_post_request()
post_request = builder.get_request()
print(post_request)
```

### Opción 2: Construcción Manual (Sin Director)

```python
from creational_patterns.builder.builder_concrete_http_request import BuilderConcreteHttpRequest

# Crear builder
builder = BuilderConcreteHttpRequest()

# Construir paso a paso
builder.reset()
builder.set_url("https://api.example.com/users")
builder.set_method("POST")
builder.set_body({"name": "Jorge", "email": "jorge@example.com"})
builder.set_timeout(30)
builder.add_header("Content-Type", "application/json")
builder.add_header("Authorization", "Bearer token123")

# Obtener el producto final
request = builder.get_request()
print(request)
```

## Cuándo Usar este Patrón

### Usar Builder Cuando:

1. **Objeto con Múltiples Configuraciones**: El objeto tiene muchas opciones de configuración
   ```python
   # Evita esto:
   request = HttpRequest(
       url="...", method="...", headers={...}, 
       body={...}, timeout=10, ssl=True, ...
   )
   
   # Usa Builder en su lugar
   ```

2. **Construcción Paso a Paso**: El proceso de construcción implica varios pasos
3. **Diferentes Representaciones**: Necesitas crear diferentes representaciones del mismo objeto
4. **Constructor Telescópico**: Tienes un constructor con muchos parámetros opcionales

### No Usar Builder Cuando:

1. El objeto es simple y tiene pocos atributos
2. El objeto no tiene configuraciones opcionales
3. La construcción no requiere pasos específicos

## Comparación con Otros Patrones

| Aspecto | Builder | Factory Method | Abstract Factory |
|---------|---------|----------------|------------------|
| **Propósito** | Construir objetos complejos paso a paso | Crear una instancia de una clase | Crear familias de objetos |
| **Complejidad** | Alta | Baja | Media-Alta |
| **Pasos** | Múltiples pasos configurables | Un solo paso | Un solo paso por producto |
| **Control** | Control fino sobre construcción | Control sobre qué clase crear | Control sobre familias |
| **Uso típico** | Objetos con muchas opciones | Polimorfismo simple | Productos relacionados |

## Variantes del Patrón

### 1. Con Director
El director conoce "recetas" predefinidas para construcciones comunes:
```python
director.build_get_request()  # Receta predefinida
```

### 2. Sin Director
El cliente controla directamente cada paso:
```python
builder.set_url("...")
builder.set_method("GET")
# ...
```

### 3. Fluent Interface (Método Encadenado)
```python
# No implementado en este ejemplo, pero común en otros lenguajes
request = builder
    .set_url("...")
    .set_method("GET")
    .add_header("Auth", "...")
    .build()
```

## Diagrama de Flujo

```
Cliente
   │
   ├─► BuilderDirector (opcional)
   │      │
   │      └─► BuilderConcreteHttpRequest
   │              │
   └──────────────┘
                  │
                  ├─► reset()
                  ├─► set_url()
                  ├─► set_method()
                  ├─► add_header()
                  ├─► set_body()
                  ├─► set_timeout()
                  │
                  └─► get_request() → HttpRequest
```

## Ejemplo Real: Constructor de Consultas SQL

```python
# Ejemplo conceptual de otro uso del Builder
query = SQLQueryBuilder()
    .select("name", "email")
    .from_table("users")
    .where("age > 18")
    .order_by("name")
    .limit(10)
    .build()
```

## Referencias

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns) (Gang of Four)
- [Refactoring Guru - Builder Pattern](https://refactoring.guru/design-patterns/builder)
- [Effective Java - Item 2: Consider a builder when faced with many constructor parameters](https://www.oreilly.com/library/view/effective-java/9780134686097/)

## Ver También

- [TUTORIAL.md](./TUTORIAL.md) - Tutorial paso a paso con ejemplos detallados
- [Abstract Factory Pattern](../abstract_factory/) - Para crear familias de objetos relacionados
- [Factory Method Pattern](../factory_method/) - Para crear objetos simples

## Ejecutar el Ejemplo

```bash
cd /home/jorge/Documents/projects/design-patterns
python -m creational_patterns.builder.main
```

## Salida Esperada

```
HttpRequest(url=https://example.com, method=GET, headers={}, body={}, timeout=10)
HttpRequest(url=https://example.com, method=POST, headers={'Authorization': 'Bearer 1234567890'}, body={'key': 'value'}, timeout=10)
HttpRequest(url=https://example.com, method=PUT, headers={'Authorization': 'Bearer 1234567890'}, body={'key': 'value'}, timeout=10)
HttpRequest(url=https://example.com, method=GET, headers={'Authorization': 'Bearer 1234567890'}, body={}, timeout=10)
```
