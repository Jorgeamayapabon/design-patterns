# Tutorial: Patrón Builder (Constructor)

## Índice

1. [Introducción](#introducción)
2. [Problema que Resuelve](#problema-que-resuelve)
3. [Solución con Builder](#solución-con-builder)
4. [Implementación Paso a Paso](#implementación-paso-a-paso)
5. [Ejecutando el Ejemplo](#ejecutando-el-ejemplo)
6. [Builder vs Constructor Tradicional](#builder-vs-constructor-tradicional)
7. [El Rol del Director](#el-rol-del-director)
8. [Patrones Relacionados](#patrones-relacionados)
9. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## Introducción

El patrón **Builder** es un patrón de diseño creacional que te permite construir objetos complejos paso a paso. Imagina que estás construyendo una casa: no la construyes toda de una vez, sino que primero pones los cimientos, luego las paredes, el techo, las ventanas, etc. El patrón Builder aplica este mismo concepto a la programación.

## Problema que Resuelve

### Escenario 1: El Constructor Telescópico

```python
class HttpRequest:
    def __init__(
        self, 
        url: str,
        method: str = "GET",
        headers: dict = None,
        body: dict = None,
        timeout: int = 30,
        ssl_verify: bool = True,
        auth: tuple = None,
        cookies: dict = None,
        # ... más parámetros
    ):
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.body = body
        self.timeout = timeout
        # ... etc

# Uso: muy confuso y propenso a errores
request = HttpRequest(
    "https://api.com",
    "POST",
    {"Content-Type": "application/json"},
    {"data": "value"},
    30,
    True,
    ("user", "pass"),
    None  # ¿Qué es este None?
)
```

**Problemas:**
- Difícil de leer y entender
- El orden de los parámetros es crítico
- Muchos parámetros opcionales requieren valores None
- Fácil cometer errores

### Escenario 2: Setters Simples

```python
class HttpRequest:
    def __init__(self):
        self.url = None
        self.method = None
        # ...

# Uso: verboso y sin validación
request = HttpRequest()
request.url = "https://api.com"
request.method = "POST"
request.headers = {"Content-Type": "application/json"}
# ¿Olvidé algo importante?
# ¿El objeto está completo y válido?
```

**Problemas:**
- No hay validación de que el objeto esté completo
- No hay control sobre el orden de configuración
- No hay encapsulación del proceso de construcción

## Solución con Builder

### Diagrama Conceptual

```
┌─────────────────────────────────────────────────┐
│               Cliente                            │
└────────────┬────────────────────────────────────┘
             │
             │ usa
             ▼
┌────────────────────────┐         ┌─────────────────────┐
│  BuilderDirector       │   usa   │  IBuilderHttpRequest│
│  (Opcional)            │────────►│  (Interfaz)         │
│ ──────────────────────│         │ ─────────────────── │
│ + build_get_request() │         │ + reset()           │
│ + build_post_request()│         │ + set_url()         │
│ + build_put_request() │         │ + set_method()      │
└────────────────────────┘         │ + set_body()        │
                                   │ + add_header()      │
                                   └──────────┬──────────┘
                                              │
                                              │ implementa
                                              ▼
                                   ┌─────────────────────────┐
                                   │BuilderConcreteHttpRequest│
                                   │ ──────────────────────── │
                                   │ + reset()                │
                                   │ + set_url()              │
                                   │ + ...                    │
                                   │ + get_request()          │
                                   └──────────┬───────────────┘
                                              │
                                              │ construye
                                              ▼
                                   ┌─────────────────────────┐
                                   │    HttpRequest          │
                                   │    (Producto)           │
                                   └─────────────────────────┘
```

## Implementación Paso a Paso

### Paso 1: Definir el Producto

Primero, creamos la clase compleja que queremos construir.

**`http_request.py`**
```python
class HttpRequest:
    """
    Producto: el objeto complejo que queremos construir.
    Tiene múltiples atributos opcionales.
    """
    _url: str
    _method: str
    _headers: dict = {}
    _body: dict = {}
    _timeout: int

    def set_url(self, url: str):
        self._url = url
    
    def set_method(self, method: str):
        self._method = method
    
    def set_headers(self, headers: dict):
        self._headers = headers
    
    def set_body(self, body: dict):
        self._body = body
    
    def set_timeout(self, timeout: int):
        self._timeout = timeout

    def __repr__(self) -> str:
        return (f"HttpRequest(url={self._url}, method={self._method}, "
                f"headers={self._headers}, body={self._body}, "
                f"timeout={self._timeout})")
```

**Nota**: El producto es una clase simple con setters. La complejidad está en el proceso de construcción, no en el producto mismo.

### Paso 2: Definir la Interfaz del Builder

La interfaz define todos los pasos posibles para construir el producto.

**`builder_http_request.py`**
```python
from abc import ABC, abstractmethod

class IBuilderHttpRequest(ABC):
    """
    Interfaz Builder: define los pasos para construir un HttpRequest.
    Cada método corresponde a una parte del producto.
    """
    
    @abstractmethod
    def reset(self) -> None:
        """Reinicia el builder para crear un nuevo producto"""
        pass

    @abstractmethod
    def set_url(self, url: str) -> None:
        """Establece la URL de la petición"""
        pass

    @abstractmethod
    def set_method(self, method: str) -> None:
        """Establece el método HTTP (GET, POST, PUT, etc.)"""
        pass

    @abstractmethod
    def set_body(self, body: dict) -> None:
        """Establece el cuerpo de la petición"""
        pass

    @abstractmethod
    def set_timeout(self, timeout: int) -> None:
        """Establece el timeout en segundos"""
        pass
    
    @abstractmethod
    def add_header(self, key: str, value: str) -> None:
        """Agrega un header a la petición"""
        pass
```

**¿Por qué una interfaz?** Permite tener múltiples builders diferentes (por ejemplo, uno que construye HttpRequest y otro que construye una representación JSON del request).

### Paso 3: Implementar el Builder Concreto

El builder concreto implementa los pasos de construcción.

**`builder_concrete_http_request.py`**
```python
from builder_http_request import IBuilderHttpRequest
from http_request import HttpRequest

class BuilderConcreteHttpRequest(IBuilderHttpRequest):
    """
    Builder Concreto: implementa los pasos para construir un HttpRequest.
    Mantiene una referencia al producto que está construyendo.
    """
    _request: HttpRequest
    _headers: dict

    def reset(self) -> None:
        """Inicializa un nuevo producto"""
        self._request = HttpRequest()
        self._headers = {}

    def set_url(self, url: str) -> None:
        self._request.set_url(url)

    def set_method(self, method: str) -> None:
        self._request.set_method(method)

    def set_body(self, body: dict) -> None:
        self._request.set_body(body)
    
    def set_timeout(self, timeout: int) -> None:
        self._request.set_timeout(timeout)

    def add_header(self, key: str, value: str) -> None:
        """
        Acumula headers en un diccionario antes de establecerlos.
        Este es un ejemplo de lógica específica del builder.
        """
        self._headers[key] = value
        self._request.set_headers(self._headers)
    
    def get_request(self) -> HttpRequest:
        """Retorna el producto construido"""
        return self._request
```

**Puntos Clave:**
- El builder mantiene una referencia al producto que está construyendo
- Cada método configura una parte específica del producto
- El método `get_request()` retorna el producto final
- `reset()` permite reutilizar el builder para crear múltiples productos

### Paso 4: Crear el Director (Opcional)

El director encapsula "recetas" para construir configuraciones específicas.

**`builder_director.py`**
```python
from builder_http_request import IBuilderHttpRequest

class BuilderDirector:
    """
    Director: conoce recetas específicas para construir productos.
    Opcional, pero útil para construcciones comunes.
    """
    _builder: IBuilderHttpRequest

    def __init__(self, builder: IBuilderHttpRequest):
        self._builder = builder
    
    def change_builder(self, builder: IBuilderHttpRequest):
        """Permite cambiar el builder en tiempo de ejecución"""
        self._builder = builder
    
    def build_get_request(self):
        """Receta para construir una petición GET simple"""
        self._builder.reset()
        self._builder.set_url("https://example.com")
        self._builder.set_method("GET")
        self._builder.set_timeout(10)
    
    def build_post_request(self):
        """Receta para construir una petición POST con autenticación"""
        self._builder.reset()
        self._builder.set_url("https://example.com")
        self._builder.set_method("POST")
        self._builder.set_body({"key": "value"})
        self._builder.set_timeout(10)
        self._builder.add_header("Authorization", "Bearer 1234567890")

    def build_put_request(self):
        """Receta para construir una petición PUT"""
        self._builder.reset()
        self._builder.set_url("https://example.com")
        self._builder.set_method("PUT")
        self._builder.set_body({"key": "value"})
        self._builder.set_timeout(10)
        self._builder.add_header("Authorization", "Bearer 1234567890")
```

**¿Cuándo usar el Director?**
- ✅ Cuando tienes configuraciones comunes y repetitivas
- ✅ Cuando quieres encapsular el conocimiento de cómo construir algo
- ❌ Cuando cada construcción es única y personalizada

### Paso 5: Usar el Builder

**`main.py`**
```python
from builder_concrete_http_request import BuilderConcreteHttpRequest
from builder_director import BuilderDirector
from http_request import HttpRequest

def run():
    # Crear instancias
    builder = BuilderConcreteHttpRequest()
    director = BuilderDirector(builder)

    # Uso 1: Con Director (construcciones predefinidas)
    print("=== Con Director ===")
    
    director.build_get_request()
    get_request = builder.get_request()
    print(get_request)

    director.build_post_request()
    post_request = builder.get_request()
    print(post_request)

    director.build_put_request()
    put_request = builder.get_request()
    print(put_request)

    # Uso 2: Sin Director (construcción personalizada)
    print("\n=== Sin Director (Manual) ===")
    
    builder.reset()
    builder.set_url("https://example.com")
    builder.set_method("GET")
    builder.set_timeout(10)
    builder.add_header("Authorization", "Bearer 1234567890")
    custom_request = builder.get_request()
    print(custom_request)

if __name__ == "__main__":
    run()
```

## Ejecutando el Ejemplo

### 1. Navegar al directorio del proyecto

```bash
cd /home/jorge/Documents/projects/design-patterns
```

### 2. Ejecutar el ejemplo

```bash
python -m creational_patterns.builder.main
```

### 3. Salida Esperada

```
=== Con Director ===
HttpRequest(url=https://example.com, method=GET, headers={}, body={}, timeout=10)
HttpRequest(url=https://example.com, method=POST, headers={'Authorization': 'Bearer 1234567890'}, body={'key': 'value'}, timeout=10)
HttpRequest(url=https://example.com, method=PUT, headers={'Authorization': 'Bearer 1234567890'}, body={'key': 'value'}, timeout=10)

=== Sin Director (Manual) ===
HttpRequest(url=https://example.com, method=GET, headers={'Authorization': 'Bearer 1234567890'}, body={}, timeout=10)
```

## Builder vs Constructor Tradicional

### Comparación Lado a Lado

#### Constructor Tradicional

```python
# Difícil de leer
request = HttpRequest(
    "https://api.com",
    "POST",
    {"Content-Type": "application/json", "Auth": "Bearer 123"},
    {"user": "jorge"},
    30
)

# ¿Qué significa cada parámetro?
# ¿Qué pasa si quiero omitir headers pero establecer timeout?
request = HttpRequest("https://api.com", "POST", None, {"user": "jorge"}, 30)
```

#### Patrón Builder

```python
# Claro y legible
request = (builder
    .reset()
    .set_url("https://api.com")
    .set_method("POST")
    .add_header("Content-Type", "application/json")
    .add_header("Authorization", "Bearer 123")
    .set_body({"user": "jorge"})
    .set_timeout(30)
    .get_request())

# Flexible: omite lo que no necesitas
request = (builder
    .reset()
    .set_url("https://api.com")
    .set_method("GET")
    .set_timeout(10)
    .get_request())
```

## El Rol del Director

### Sin Director (Control Total)

```python
# El cliente controla cada paso
builder.reset()
builder.set_url("https://api.example.com/users")
builder.set_method("POST")
builder.add_header("Content-Type", "application/json")
builder.add_header("Authorization", "Bearer token123")
builder.set_body({"name": "Jorge", "email": "jorge@example.com"})
builder.set_timeout(30)
request = builder.get_request()
```

**Ventajas:**
- Control total sobre la construcción
- Flexibilidad máxima

**Desventajas:**
- Código repetitivo si se usa el mismo patrón múltiples veces
- Fácil olvidar pasos importantes

### Con Director (Recetas Predefinidas)

```python
# El director encapsula la lógica de construcción
director.build_authenticated_post_request()
request = builder.get_request()
```

**Ventajas:**
- Código más limpio y mantenible
- Garantiza que no se olviden pasos
- Reutilización de configuraciones comunes

**Desventajas:**
- Menos flexible
- Necesitas modificar el director para nuevas configuraciones

### ¿Cuándo Usar Cada Uno?

| Escenario | Usar Director | Usar Builder Directo |
|-----------|---------------|---------------------|
| Configuraciones estándar repetitivas | ✅ | ❌ |
| Construcciones únicas y personalizadas | ❌ | ✅ |
| API pública con casos de uso comunes | ✅ | ❌ |
| Experimentación y prototipado | ❌ | ✅ |
| Balance entre los dos | ✅ (con opción manual) | ✅ |

## Patrones Relacionados

### Builder vs Factory Method

```python
# Factory Method: crea el objeto completo de una vez
class RequestFactory:
    @staticmethod
    def create_get_request(url: str) -> HttpRequest:
        return HttpRequest(url, "GET", timeout=10)

# Builder: construcción paso a paso con control fino
builder.set_url(url)
builder.set_method("GET")
builder.set_timeout(10)
request = builder.get_request()
```

**Usa Factory Method cuando:** La creación es simple y de un solo paso
**Usa Builder cuando:** La construcción es compleja y requiere múltiples pasos

### Builder vs Abstract Factory

```python
# Abstract Factory: crea familias de objetos relacionados
factory = AwsFactory()
email_sender = factory.create_email_sender()
sms_sender = factory.create_sms_sender()

# Builder: construye un solo objeto complejo
builder.set_url("...")
builder.set_method("POST")
request = builder.get_request()
```

**Usa Abstract Factory cuando:** Necesitas crear múltiples objetos relacionados
**Usa Builder cuando:** Necesitas construir un objeto complejo paso a paso

## Ejercicios Prácticos

### Ejercicio 1: Agregar Validación

Modifica el builder para que valide que los campos requeridos estén presentes antes de retornar el producto:

```python
def get_request(self) -> HttpRequest:
    if not self._request._url:
        raise ValueError("URL es requerida")
    if not self._request._method:
        raise ValueError("Método HTTP es requerido")
    return self._request
```

### Ejercicio 2: Implementar Fluent Interface

Modifica el builder para que retorne `self` en cada método, permitiendo encadenamiento:

```python
def set_url(self, url: str) -> 'BuilderConcreteHttpRequest':
    self._request.set_url(url)
    return self

# Uso:
request = (builder.reset()
    .set_url("...")
    .set_method("GET")
    .get_request())
```

### Ejercicio 3: Builder para Emails

Crea un builder para construir objetos Email:

```python
class Email:
    def __init__(self):
        self.to = []
        self.cc = []
        self.bcc = []
        self.subject = ""
        self.body = ""
        self.attachments = []
        self.priority = "normal"

# Implementa:
# - IEmailBuilder (interfaz)
# - EmailBuilder (builder concreto)
# - EmailDirector (con recetas como: welcome_email, notification_email)
```

### Ejercicio 4: Builder para Consultas SQL

Crea un builder que construya consultas SQL:

```python
query = (SQLQueryBuilder()
    .select("name", "email", "age")
    .from_table("users")
    .where("age >= 18")
    .where("country = 'MX'")
    .order_by("name", "ASC")
    .limit(10)
    .build())

# Resultado: 
# "SELECT name, email, age FROM users WHERE age >= 18 AND country = 'MX' 
#  ORDER BY name ASC LIMIT 10"
```

### Ejercicio 5: Builder con Inmutabilidad

Crea una versión del builder que produzca objetos inmutables:

```python
class ImmutableHttpRequest:
    def __init__(self, url: str, method: str, headers: dict, body: dict, timeout: int):
        self._url = url
        self._method = method
        self._headers = headers.copy()  # Copia defensiva
        self._body = body.copy()
        self._timeout = timeout
    
    # Solo getters, sin setters
    @property
    def url(self) -> str:
        return self._url
```

## Variaciones Avanzadas

### 1. Builder con Caché

```python
class CachedBuilder(BuilderConcreteHttpRequest):
    def __init__(self):
        super().__init__()
        self._cache = {}
    
    def get_request(self) -> HttpRequest:
        key = f"{self._request._url}_{self._request._method}"
        if key not in self._cache:
            self._cache[key] = super().get_request()
        return self._cache[key]
```

### 2. Builder con Clonación

```python
class CloneableBuilder(BuilderConcreteHttpRequest):
    def clone(self) -> 'CloneableBuilder':
        """Crea una copia del builder en su estado actual"""
        new_builder = CloneableBuilder()
        new_builder._request = copy.deepcopy(self._request)
        new_builder._headers = self._headers.copy()
        return new_builder

# Uso:
base_builder = CloneableBuilder()
base_builder.set_url("https://api.com")
base_builder.set_timeout(30)

# Crear variaciones a partir de la base
get_builder = base_builder.clone().set_method("GET")
post_builder = base_builder.clone().set_method("POST")
```

## Conclusiones Clave

1. **Separación de Preocupaciones**: El Builder separa la construcción de la representación
2. **Flexibilidad**: Permite crear diferentes representaciones del mismo producto
3. **Legibilidad**: El código es más fácil de leer que constructores con muchos parámetros
4. **Control**: Tienes control total sobre cada paso del proceso de construcción
5. **Reutilización**: El director permite reutilizar recetas de construcción
6. **Testabilidad**: Es fácil crear builders mock para pruebas

## Próximos Pasos

- Implementa un builder con Fluent Interface
- Crea un builder para otro dominio (Emails, Documentos, Configuraciones)
- Compara el patrón Builder con otros patrones creacionales
- Estudia el patrón Prototype que también se usa para crear objetos complejos

## Preguntas para Reflexionar

1. ¿Cuándo preferirías un simple constructor sobre un Builder?
2. ¿Cómo manejarías dependencias entre pasos de construcción?
3. ¿Qué ventajas tiene el Builder sobre un objeto con todos los setters públicos?
4. ¿Cómo implementarías un builder que valide el orden de los pasos?

---

**¡Felicidades!** 🎉 Ahora dominas el patrón Builder y puedes construir objetos complejos de manera elegante y mantenible.
