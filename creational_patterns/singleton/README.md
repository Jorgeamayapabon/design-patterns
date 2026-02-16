# Patrón Singleton - Configuración de Base de Datos

## Descripción

Este ejemplo demuestra el uso del patrón **Singleton** para gestionar la configuración de conexión a una base de datos PostgreSQL. El patrón garantiza que solo exista una instancia de configuración en toda la aplicación.

## Estructura de archivos

```
singleton/
├── decorator.py      # Decorador @singleton reutilizable
├── db.py            # Implementación de DatabaseConfig con Singleton
├── main.py          # Casos de uso y ejemplos
└── README.md        # Esta documentación
```

## ¿Por qué usar Singleton para configuración de DB?

### Ventajas

- **Instancia única**: Solo se leen las variables de entorno una vez  
- **Consistencia**: Todos los módulos usan la misma configuración  
- **Eficiencia**: Evita múltiples lecturas de variables de entorno  
- **Acceso global**: Fácil acceso desde cualquier parte de la aplicación  

### Casos de uso apropiados

- Configuración de aplicación
- Gestión de conexiones a base de datos
- Loggers centralizados
- Gestores de caché
- Pool de conexiones

## Configuración

### Variables de entorno

El ejemplo utiliza las siguientes variables de entorno con sus valores por defecto:

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DB_HOST` | `localhost` | Host del servidor PostgreSQL |
| `DB_PORT` | `5432` | Puerto de PostgreSQL |
| `DB_USER` | `postgres` | Usuario de la base de datos |
| `DB_PASSWORD` | `postgres` | Contraseña del usuario |
| `DB_NAME` | `mydatabase` | Nombre de la base de datos |

### Ejemplo de configuración

```bash
# Configuración de desarrollo (por defecto)
python creational_patterns/singleton/main.py

# Configuración personalizada
export DB_HOST=production-db.example.com
export DB_PORT=5433
export DB_USER=app_user
export DB_PASSWORD=secure_password
export DB_NAME=production_db
python creational_patterns/singleton/main.py
```

## Uso del código

### Implementar el Singleton (ya implementado)

```python
# decorator.py
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
```

### Aplicar el decorador

```python
# db.py
from creational_patterns.singleton.decorator import singleton

@singleton
class DatabaseConfig:
    def __init__(self):
        self._host = os.getenv('DB_HOST', 'localhost')
        # ... más configuración
```

### Usar la configuración

```python
# En cualquier módulo de tu aplicación
from creational_patterns.singleton.db import DatabaseConfig

config = DatabaseConfig()
connection_string = config.get_connection_string()
```

## Ejecutar los ejemplos

```bash
# Desde la raíz del proyecto
python -m creational_patterns.singleton.main

# O directamente
python creational_patterns/singleton/main.py
```

## Ejemplos incluidos

El archivo `main.py` incluye 4 ejemplos didácticos:

1. **Instancia única**: Demuestra que múltiples llamadas retornan la misma instancia
2. **Acceso a configuración**: Cómo acceder a los parámetros y generar cadenas de conexión
3. **Uso práctico**: Simula múltiples módulos accediendo a la configuración
4. **Variables de entorno**: Muestra cómo configurar usando variables de entorno

## API de DatabaseConfig

### Propiedades

- `host` - Host del servidor PostgreSQL
- `port` - Puerto del servidor
- `user` - Usuario de la base de datos
- `password` - Contraseña del usuario
- `database` - Nombre de la base de datos

### Métodos

- `get_connection_string(hide_password=True)` - Genera URI de conexión PostgreSQL
- `get_connection_dict()` - Retorna diccionario con parámetros de conexión

## Consideraciones

### Thread-Safety

**Importante**: Esta implementación del decorador Singleton **NO es thread-safe**. Para aplicaciones multi-threading, considera usar:

```python
import threading

def singleton(cls):
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance
```

### Testing

Para tests unitarios, considera resetear el singleton entre tests o usar dependency injection para mayor testabilidad.

## Recursos adicionales

- [Wikipedia - Singleton Pattern](https://en.wikipedia.org/wiki/Singleton_pattern)
- [Refactoring Guru - Singleton](https://refactoring.guru/design-patterns/singleton)
- [Python Design Patterns](https://python-patterns.guide/gang-of-four/singleton/)

## Licencia

Código de ejemplo con propósitos educativos.
