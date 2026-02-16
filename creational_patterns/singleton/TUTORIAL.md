# Tutorial: Patrón Singleton con PostgreSQL

## Objetivo

Aprender a implementar el patrón Singleton de forma productiva usando un decorador de clase, aplicado a la configuración de una base de datos PostgreSQL.

## ¿Qué es el Patrón Singleton?

El patrón Singleton es un patrón de diseño creacional que **garantiza que una clase tenga solo una instancia** y proporciona un punto de acceso global a ella.

### Problema que resuelve

Imagina que tienes una aplicación con múltiples módulos que necesitan acceder a la configuración de la base de datos:

```python
# ❌ Sin Singleton: múltiples lecturas de variables de entorno
# módulo_a.py
config_a = DatabaseConfig()  # Lee las env vars

# módulo_b.py
config_b = DatabaseConfig()  # Lee las env vars otra vez

# módulo_c.py
config_c = DatabaseConfig()  # Lee las env vars nuevamente
```

Cada módulo crea su propia instancia, lo que resulta en:
- ❌ Múltiples lecturas de variables de entorno
- ❌ Uso ineficiente de memoria
- ❌ Posibles inconsistencias si la configuración cambia

### Solución con Singleton

```python
# Con Singleton: una única instancia compartida
# módulo_a.py
config_a = DatabaseConfig()  # Crea la instancia

# módulo_b.py
config_b = DatabaseConfig()  # Retorna la misma instancia

# módulo_c.py
config_c = DatabaseConfig()  # Retorna la misma instancia

# Todas son la misma instancia en memoria
assert config_a is config_b is config_c  # True
```

## 🔧 Implementación

### Paso 1: Crear el decorador Singleton

El decorador es reutilizable para cualquier clase:

```python
# decorator.py
def singleton(cls):
    """
    Decorador que convierte cualquier clase en un Singleton.
    
    Uso:
        @singleton
        class MiClase:
            pass
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance
```

**¿Cómo funciona?**
1. `instances` es un diccionario que guarda las instancias creadas
2. La primera vez que se llama, crea la instancia y la guarda
3. Las siguientes veces, retorna la instancia guardada

### Paso 2: Aplicar el decorador a DatabaseConfig

```python
# db.py
import os
from creational_patterns.singleton.decorator import singleton

@singleton
class DatabaseConfig:
    """
    Configuración Singleton para PostgreSQL.
    Solo se inicializa una vez en toda la aplicación.
    """
    
    def __init__(self):
        # Leer variables de entorno (solo se ejecuta una vez)
        self._host = os.getenv('DB_HOST', 'localhost')
        self._port = int(os.getenv('DB_PORT', '5432'))
        self._user = os.getenv('DB_USER', 'postgres')
        self._password = os.getenv('DB_PASSWORD', 'postgres')
        self._database = os.getenv('DB_NAME', 'mydatabase')
        
        print(f"[Singleton] Configuración inicializada para: {self._host}:{self._port}")
    
    # Propiedades para acceder a la configuración
    @property
    def host(self) -> str:
        return self._host
    
    # ... más propiedades
    
    def get_connection_string(self, hide_password: bool = True) -> str:
        """Genera la URI de conexión para PostgreSQL."""
        password = "****" if hide_password else self._password
        return f"postgresql://{self._user}:{password}@{self._host}:{self._port}/{self._database}"
```

### Paso 3: Usar la configuración

```python
# main.py
from creational_patterns.singleton.db import DatabaseConfig

# En cualquier parte de tu aplicación
config = DatabaseConfig()
print(config.get_connection_string())
# Output: postgresql://postgres:****@localhost:5432/mydatabase
```

## 🎓 Ejemplos Didácticos

### Ejemplo 1: Verificar instancia única

```python
def ejemplo_1_instancia_unica():
    config1 = DatabaseConfig()  # Primera llamada: inicializa
    config2 = DatabaseConfig()  # Segunda llamada: retorna la misma
    config3 = DatabaseConfig()  # Tercera llamada: retorna la misma
    
    print(f"config1 is config2: {config1 is config2}")  # True
    print(f"config2 is config3: {config2 is config3}")  # True
    print(f"Mismo ID de memoria: {id(config1) == id(config2)}")  # True
```

### Ejemplo 2: Múltiples módulos

```python
# modulo_conexion.py
def conectar_db():
    config = DatabaseConfig()
    print(f"Conectando a: {config.get_connection_string()}")

# modulo_migracion.py
def ejecutar_migracion():
    config = DatabaseConfig()  # Misma instancia que conectar_db
    print(f"Migración en: {config.database}")

# modulo_backup.py
def hacer_backup():
    config = DatabaseConfig()  # Misma instancia que los anteriores
    print(f"Backup de: {config.database}")
```

## Casos de Uso Apropiados

### Cuándo usar Singleton

1. **Configuración de aplicación**
   - Parámetros de configuración global
   - Conexiones a base de datos
   - Configuración de API keys

2. **Recursos compartidos**
   - Loggers centralizados
   - Pool de conexiones
   - Caché en memoria

3. **Gestores únicos**
   - Gestores de estado global
   - Coordinadores de recursos
   - Administradores de eventos

### Cuándo NO usar Singleton

1. **Clases con estado mutable frecuente**
   - Dificulta el testing
   - Problemas de concurrencia

2. **Cuando necesitas múltiples instancias**
   - Diferentes configuraciones por contexto
   - Testing con mocks

3. **Clases sin estado**
   - Mejor usar funciones o métodos estáticos

## Consideraciones Importantes

### Thread-Safety

La implementación básica **NO es thread-safe**. Para aplicaciones multi-threading:

```python
import threading

def singleton(cls):
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                # Double-checked locking
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance
```

### Testing

El Singleton puede dificultar los tests. Soluciones:

1. **Resetear entre tests:**
```python
def reset_singleton():
    DatabaseConfig._instances.clear()
```

2. **Usar dependency injection:**
```python
def mi_funcion(config=None):
    if config is None:
        config = DatabaseConfig()
    # usar config
```

3. **Mock en tests:**
```python
from unittest.mock import patch

@patch('mi_modulo.DatabaseConfig')
def test_mi_funcion(mock_config):
    # test con mock
    pass
```

## Ventajas y Desventajas

### Ventajas

1. **Garantiza instancia única** - Control estricto sobre la instancia
2. **Acceso global** - Fácil acceso desde cualquier parte
3. **Inicialización lazy** - Se crea solo cuando se necesita
4. **Eficiencia** - Ahorra recursos (memoria, I/O)

### Desventajas

1. **Viola el principio de responsabilidad única** - Controla su instanciación
2. **Dificulta el testing** - Estado global compartido
3. **Oculta dependencias** - No están explícitas en firmas de funciones
4. **Problemas de concurrencia** - Requiere implementación thread-safe

## Buenas Prácticas

1. **Usa el decorador** - Más limpio que implementar `__new__`
2. **Documenta claramente** - Explica por qué es Singleton
3. **Considera alternativas** - Dependency injection puede ser mejor
4. **Hazlo thread-safe** - Si tu app es multi-threading
5. **Úsalo con moderación** - Solo cuando realmente lo necesites

## Ejecutar el Ejemplo

```bash
# Con configuración por defecto
python3 -m creational_patterns.singleton.main

# Con configuración personalizada
export DB_HOST=production-db.example.com
export DB_PORT=5433
export DB_USER=app_user
export DB_PASSWORD=secure_password
export DB_NAME=production_db
python3 -m creational_patterns.singleton.main
```

## 📖 Recursos Adicionales

- [Refactoring Guru - Singleton](https://refactoring.guru/design-patterns/singleton)
- [Python Patterns - Singleton](https://python-patterns.guide/gang-of-four/singleton/)
- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns)

## Ejercicios Propuestos

1. Modifica el decorador para hacerlo thread-safe
2. Implementa un Logger Singleton con niveles de log
3. Crea un CacheManager Singleton con límite de memoria
4. Implementa reset del Singleton para testing
5. Compara Singleton vs. Módulo Python (ambos son singletons naturales)

---

¡Felicidades! Ahora entiendes cómo implementar y usar el patrón Singleton de forma productiva en Python. 🎉
