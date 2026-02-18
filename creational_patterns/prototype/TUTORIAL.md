# Tutorial: Patrón Prototype (Prototipo)

## Índice

1. [Introducción](#introducción)
2. [Problema que Resuelve](#problema-que-resuelve)
3. [Solución con Prototype](#solución-con-prototype)
4. [Implementación Paso a Paso](#implementación-paso-a-paso)
5. [Ejecutando el Ejemplo](#ejecutando-el-ejemplo)
6. [Deep Copy vs Shallow Copy](#deep-copy-vs-shallow-copy)
7. [Registro de Prototipos](#registro-de-prototipos)
8. [Casos de Uso Avanzados](#casos-de-uso-avanzados)
9. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## Introducción

El patrón **Prototype** es como tener un "molde" o "plantilla" que puedes duplicar tantas veces como necesites. En lugar de crear objetos desde cero cada vez, clonas una instancia existente y la modificas según tus necesidades.

**Analogía del Mundo Real**: Piensa en una fábrica de galletas. En lugar de preparar la masa desde cero cada vez, tienes una masa base (el prototipo) que copias y luego personalizas con diferentes ingredientes.

## Problema que Resuelve

### Escenario Sin Prototype

Imagina que necesitas crear múltiples configuraciones de jobs con parámetros similares:

```python
# Crear cada job desde cero es tedioso
job1 = JobConfig(
    name="data-processor-1",
    retries=5,
    timeout=30,
    metadata={
        "priority": "low",
        "environment": "production",
        "team": "data-science",
        "notifications": ["email", "slack"]
    }
)

job2 = JobConfig(
    name="data-processor-2",
    retries=5,  # ¡Mismo valor!
    timeout=30,  # ¡Mismo valor!
    metadata={
        "priority": "low",  # ¡Mismo valor!
        "environment": "production",  # ¡Mismo valor!
        "team": "data-science",  # ¡Mismo valor!
        "notifications": ["email", "slack"]  # ¡Mismo valor!
    }
)

job3 = JobConfig(
    name="data-processor-3",
    retries=5,  # ¡Repetición!
    timeout=30,
    metadata={
        "priority": "low",
        "environment": "production",
        "team": "data-science",
        "notifications": ["email", "slack"]
    }
)
```

### Problemas Identificados

1. **Código Repetitivo**: Los mismos valores se repiten múltiples veces
2. **Propenso a Errores**: Fácil olvidar un campo o escribir un valor incorrecto
3. **Difícil de Mantener**: Si necesitas cambiar la configuración base, debes cambiarla en todos lados
4. **Ineficiente**: Crear objetos complejos desde cero puede ser costoso

### Con Factory?

```python
class JobConfigFactory:
    @staticmethod
    def create_data_processor(name: str) -> JobConfig:
        return JobConfig(
            name=name,
            retries=5,
            timeout=30,
            metadata={"priority": "low", ...}
        )

# Mejor, pero aún necesitas una factory para cada tipo
job1 = JobConfigFactory.create_data_processor("processor-1")
job2 = JobConfigFactory.create_data_processor("processor-2")

# ¿Y si necesitas crear una variación? Nueva factory
class JobConfigFactory:
    @staticmethod
    def create_fast_processor(name: str): ...
    
    @staticmethod
    def create_safe_processor(name: str): ...
    
    @staticmethod
    def create_critical_processor(name: str): ...
    # ¡Explosión de métodos!
```

## Solución con Prototype

### Diagrama Conceptual

```
┌────────────────────────────────────────┐
│  1. Registrar Prototipos               │
│     (Una sola vez)                     │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│  JobTemplates                          │
│  ┌──────────────────────────────────┐ │
│  │ "fast"  → JobConfig(retries=1)   │ │
│  │ "safe"  → JobConfig(retries=5)   │ │
│  │ "custom"→ JobConfig(retries=10)  │ │
│  └──────────────────────────────────┘ │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│  2. Obtener Copias                     │
│     (Cada vez que necesites)           │
│                                        │
│  job1 = JobTemplates.get("fast")      │
│  job2 = JobTemplates.get("safe")      │
│                                        │
│  ✓ Rápido                              │
│  ✓ Consistente                         │
│  ✓ Fácil de personalizar               │
└────────────────────────────────────────┘
```

## Implementación Paso a Paso

### Paso 1: Definir la Interfaz Prototype

Primero, definimos la interfaz que todos los prototipos deben implementar.

**`prototype_job.py`**
```python
from abc import ABC, abstractmethod
from typing import Any

class IPrototypeJob(ABC):
    """
    Interfaz Prototype: define el contrato para objetos clonables.
    Solo requiere un método: clone()
    """
    
    @abstractmethod
    def clone(self) -> Any:
        """
        Crea y retorna una copia del objeto.
        
        Returns:
            Una copia independiente del objeto
        """
        pass
```

**¿Por qué una interfaz?** Garantiza que todos los prototipos puedan ser clonados de manera uniforme.

### Paso 2: Implementar el Prototipo Concreto

Ahora implementamos una clase concreta que puede clonarse.

**`config.py`**
```python
from prototype_job import IPrototypeJob
from typing import Any, Dict
import copy

class JobConfig(IPrototypeJob):
    """
    Prototipo Concreto: un objeto que puede clonarse a sí mismo.
    """
    
    def __init__(
        self, 
        name: str, 
        retries: int, 
        timeout: int, 
        metadata: Dict[str, Any]
    ):
        self._name = name
        self._retries = retries
        self._timeout = timeout
        self.metadata = metadata  # Público para modificación después de clonar

    def clone(self) -> "JobConfig":
        """
        Implementación del método clone usando deep copy.
        
        Deep copy crea una copia completamente independiente,
        incluyendo todos los objetos anidados (como metadata).
        """
        return copy.deepcopy(self)

    def __repr__(self):
        return (
            f"JobConfig(name={self._name!r}, "
            f"retries={self._retries!r}, "
            f"timeout={self._timeout!r}, "
            f"metadata={self.metadata!r})"
        )
```

**Puntos Clave:**
- `copy.deepcopy()` crea una copia profunda del objeto
- Los atributos privados (`_name`, `_retries`) están encapsulados
- `metadata` es público para permitir personalizaciones post-clonación

### Paso 3: Crear el Registro de Prototipos

El registro almacena y gestiona los prototipos.

**`templates.py`**
```python
from typing import Dict
from config import JobConfig

class JobTemplates:
    """
    Registro de Prototipos: almacena y proporciona acceso a prototipos.
    
    Este es el patrón Registry, comúnmente usado con Prototype.
    """
    _templates: Dict[str, JobConfig] = {}

    @classmethod
    def register(cls, key: str, template: JobConfig) -> None:
        """
        Registra un prototipo con una clave única.
        
        Args:
            key: Identificador único para el template
            template: El prototipo a almacenar
        """
        cls._templates[key] = template

    @classmethod
    def get(cls, key: str) -> JobConfig:
        """
        Obtiene una COPIA del prototipo especificado.
        
        Args:
            key: Identificador del template
            
        Returns:
            Una copia independiente del prototipo
            
        Raises:
            ValueError: Si el key no existe
        """
        if key not in cls._templates:
            raise ValueError(f"Template with key {key} not found")
        
        # ¡IMPORTANTE! Retorna una copia, no el original
        return cls._templates[key].clone()
```

**¿Por qué clonar en `get()`?** Para proteger el prototipo original de modificaciones accidentales.

### Paso 4: Usar el Sistema de Prototipos

**`main.py`**
```python
from config import JobConfig
from templates import JobTemplates

def register_templates():
    """
    Registra los prototipos predefinidos.
    Esto se hace una sola vez al inicio de la aplicación.
    """
    # Prototipo "fast": para jobs rápidos con prioridad alta
    JobTemplates.register(
        "fast",
        JobConfig(
            name="fast-job",
            retries=1,
            timeout=5,
            metadata={"priority": "high"}
        )
    )
    
    # Prototipo "safe": para jobs seguros con múltiples reintentos
    JobTemplates.register(
        "safe",
        JobConfig(
            name="safe-job",
            retries=5,
            timeout=30,
            metadata={"priority": "low"}
        )
    )

def run():
    # 1. Registrar templates (una vez)
    register_templates()
    
    # 2. Obtener copias de los templates
    job1 = JobTemplates.get("fast")
    job2 = JobTemplates.get("fast")  # Otra copia del mismo template
    job3 = JobTemplates.get("safe")
    
    # 3. Personalizar las copias según necesites
    job2.metadata["priority"] = "critical"
    
    # 4. Las copias son independientes
    print(job1)  # priority: "high" (sin cambios)
    print(job2)  # priority: "critical" (modificado)
    print(job3)  # priority: "low" (sin cambios)

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
python -m creational_patterns.prototype.main
```

### 3. Salida Esperada

```
JobConfig(name='fast-job', retries=1, timeout=5, metadata={'priority': 'high'})
JobConfig(name='fast-job', retries=1, timeout=5, metadata={'priority': 'critical'})
JobConfig(name='safe-job', retries=5, timeout=30, metadata={'priority': 'low'})
```

**Análisis de la Salida:**
- `job1` mantiene su `priority` como "high"
- `job2` tiene `priority` "critical" (modificado)
- `job3` tiene sus propios valores independientes
- Esto demuestra que cada copia es independiente

## Deep Copy vs Shallow Copy

### La Diferencia Crítica

```python
import copy

# Objeto original con metadata anidada
original = JobConfig(
    name="original",
    retries=3,
    timeout=10,
    metadata={"priority": "high", "tags": ["important"]}
)
```

#### Shallow Copy

```python
# Shallow copy: copia el objeto pero comparte referencias a objetos mutables
shallow = copy.copy(original)

# Modificar metadata en la copia afecta al original
shallow.metadata["priority"] = "critical"
shallow.metadata["tags"].append("urgent")

print(original.metadata)
# Output: {'priority': 'critical', 'tags': ['important', 'urgent']}
# ¡El original cambió!
```

**Problema**: Los objetos mutables anidados (dict, list) se comparten entre el original y la copia.

#### Deep Copy

```python
# Deep copy: copia el objeto Y todos los objetos anidados
deep = copy.deepcopy(original)

# Modificar metadata en la copia NO afecta al original
deep.metadata["priority"] = "critical"
deep.metadata["tags"].append("urgent")

print(original.metadata)
# Output: {'priority': 'high', 'tags': ['important']}
# El original está intacto ✓

print(deep.metadata)
# Output: {'priority': 'critical', 'tags': ['important', 'urgent']}
# Solo la copia cambió ✓
```

### Visualización

```
Original: JobConfig
    ├─ name: "original"
    ├─ retries: 3
    └─ metadata: {...} ← Objeto en memoria A

Shallow Copy: JobConfig
    ├─ name: "original"
    ├─ retries: 3
    └─ metadata: {...} ← ¡MISMO objeto en memoria A!

Deep Copy: JobConfig
    ├─ name: "original"
    ├─ retries: 3
    └─ metadata: {...} ← DIFERENTE objeto en memoria B
```

### Cuándo Usar Cada Uno

| Tipo | Cuándo Usar | Ventaja | Desventaja |
|------|-------------|---------|------------|
| **Shallow Copy** | Objetos inmutables o cuando quieres compartir referencias | Más rápido | Referencias compartidas |
| **Deep Copy** | Objetos con atributos mutables que deben ser independientes | Copias totalmente independientes | Más lento, más memoria |

**En este proyecto usamos Deep Copy** porque queremos que cada job tenga su propio metadata independiente.

## Registro de Prototipos

El patrón Registry es un complemento común al patrón Prototype.

### Ventajas del Registry

```python
# SIN Registry
fast_prototype = JobConfig(name="fast", retries=1, timeout=5, metadata={...})

job1 = fast_prototype.clone()
job2 = fast_prototype.clone()

# Problemas:
# 1. fast_prototype está expuesto (puede ser modificado)
# 2. Cliente necesita mantener referencias a los prototipos
# 3. No hay centralización
```

```python
# CON Registry
JobTemplates.register("fast", JobConfig(...))

job1 = JobTemplates.get("fast")
job2 = JobTemplates.get("fast")

# Ventajas:
# ✓ Prototipos encapsulados
# ✓ Acceso centralizado
# ✓ Fácil de gestionar
# ✓ Protección del original
```

### Implementación Avanzada del Registry

```python
class JobTemplates:
    _templates: Dict[str, JobConfig] = {}
    
    @classmethod
    def register(cls, key: str, template: JobConfig) -> None:
        """Registra un template"""
        if key in cls._templates:
            raise ValueError(f"Template {key} already exists")
        cls._templates[key] = template
    
    @classmethod
    def unregister(cls, key: str) -> None:
        """Elimina un template"""
        if key in cls._templates:
            del cls._templates[key]
    
    @classmethod
    def get(cls, key: str) -> JobConfig:
        """Obtiene una copia del template"""
        if key not in cls._templates:
            raise ValueError(f"Template {key} not found")
        return cls._templates[key].clone()
    
    @classmethod
    def list_templates(cls) -> list[str]:
        """Lista todas las claves de templates disponibles"""
        return list(cls._templates.keys())
    
    @classmethod
    def exists(cls, key: str) -> bool:
        """Verifica si un template existe"""
        return key in cls._templates
```

## Casos de Uso Avanzados

### Caso 1: Sistema de Configuración Multi-Entorno

```python
# Configuraciones base por entorno
JobTemplates.register(
    "dev",
    JobConfig(
        name="dev-job",
        retries=1,
        timeout=10,
        metadata={
            "environment": "development",
            "logging_level": "DEBUG",
            "notifications": []
        }
    )
)

JobTemplates.register(
    "prod",
    JobConfig(
        name="prod-job",
        retries=5,
        timeout=60,
        metadata={
            "environment": "production",
            "logging_level": "ERROR",
            "notifications": ["email", "slack", "pagerduty"]
        }
    )
)

# Uso
dev_job = JobTemplates.get("dev")
dev_job.metadata["developer"] = "Jorge"

prod_job = JobTemplates.get("prod")
prod_job.metadata["release_version"] = "1.2.3"
```

### Caso 2: Gestión de Perfiles de Usuario

```python
from dataclasses import dataclass
from typing import List
import copy

@dataclass
class UserProfile(IPrototypeJob):
    username: str
    permissions: List[str]
    preferences: dict
    
    def clone(self) -> "UserProfile":
        return copy.deepcopy(self)

# Registrar perfiles por rol
UserProfiles.register(
    "admin",
    UserProfile(
        username="",
        permissions=["read", "write", "delete", "manage_users"],
        preferences={"theme": "dark", "language": "es"}
    )
)

UserProfiles.register(
    "user",
    UserProfile(
        username="",
        permissions=["read"],
        preferences={"theme": "light", "language": "es"}
    )
)

# Crear usuarios basados en perfiles
jorge = UserProfiles.get("admin")
jorge.username = "jorge"

maria = UserProfiles.get("user")
maria.username = "maria"
```

### Caso 3: Plantillas de Documentos

```python
class Document(IPrototypeJob):
    def __init__(self, title: str, sections: list, metadata: dict):
        self.title = title
        self.sections = sections
        self.metadata = metadata
    
    def clone(self) -> "Document":
        return copy.deepcopy(self)

# Templates de documentos
DocumentTemplates.register(
    "invoice",
    Document(
        title="Invoice",
        sections=["header", "items", "total", "footer"],
        metadata={
            "company": "ACME Corp",
            "address": "123 Main St",
            "tax_rate": 0.16
        }
    )
)

# Crear facturas
invoice1 = DocumentTemplates.get("invoice")
invoice1.metadata["client"] = "Client A"
invoice1.metadata["date"] = "2026-02-16"

invoice2 = DocumentTemplates.get("invoice")
invoice2.metadata["client"] = "Client B"
invoice2.metadata["date"] = "2026-02-17"
```

## Ejercicios Prácticos

### Ejercicio 1: Implementar Versionado de Prototipos

Modifica el registro para soportar múltiples versiones de un mismo template:

```python
class VersionedJobTemplates:
    _templates: Dict[str, Dict[str, JobConfig]] = {}
    
    @classmethod
    def register(cls, key: str, version: str, template: JobConfig) -> None:
        """Registra un template con versión"""
        # TODO: Implementar
        pass
    
    @classmethod
    def get(cls, key: str, version: str = "latest") -> JobConfig:
        """Obtiene un template específico o la última versión"""
        # TODO: Implementar
        pass

# Uso esperado:
VersionedJobTemplates.register("fast", "v1", JobConfig(...))
VersionedJobTemplates.register("fast", "v2", JobConfig(...))

job_v1 = VersionedJobTemplates.get("fast", "v1")
job_latest = VersionedJobTemplates.get("fast")  # Obtiene v2
```

### Ejercicio 2: Clone Personalizado para Objetos Complejos

Implementa un método clone personalizado que no use `deepcopy`:

```python
class JobConfig(IPrototypeJob):
    def __init__(self, name: str, retries: int, timeout: int, metadata: dict):
        self._name = name
        self._retries = retries
        self._timeout = timeout
        self.metadata = metadata
    
    def clone(self) -> "JobConfig":
        """
        Clone manual sin usar deepcopy.
        Útil para objetos con campos no serializables.
        """
        # TODO: Implementar clonación manual
        # Pista: crear nuevo JobConfig y copiar cada campo
        pass
```

### Ejercicio 3: Sistema de Plantillas de Email

Crea un sistema completo de plantillas de email:

```python
class Email(IPrototypeJob):
    def __init__(
        self,
        subject: str,
        body: str,
        from_address: str,
        headers: dict
    ):
        # TODO: Implementar
        pass
    
    def clone(self) -> "Email":
        # TODO: Implementar
        pass

# Crea las siguientes plantillas:
# - "welcome": Email de bienvenida
# - "password_reset": Email para resetear contraseña
# - "newsletter": Email de newsletter

# Requisitos:
# 1. Implementar la clase Email
# 2. Crear EmailTemplates (registry)
# 3. Registrar las 3 plantillas
# 4. Demostrar creación y personalización de emails
```

### Ejercicio 4: Caché de Prototipos

Implementa un sistema que almacene en caché las copias clonadas:

```python
class CachedJobTemplates:
    _templates: Dict[str, JobConfig] = {}
    _cache: Dict[str, List[JobConfig]] = {}
    _cache_size: int = 5
    
    @classmethod
    def get(cls, key: str) -> JobConfig:
        """
        Obtiene un template del cache si existe,
        o clona uno nuevo y lo agrega al cache.
        """
        # TODO: Implementar
        # 1. Verificar si hay copias en cache
        # 2. Si hay, retornar una (y eliminarla del cache)
        # 3. Si no, clonar una nueva
        # 4. Mantener el cache con tamaño máximo
        pass
    
    @classmethod
    def warm_cache(cls, key: str) -> None:
        """Pre-carga el cache con copias"""
        # TODO: Implementar
        pass
```

### Ejercicio 5: Prototipos con Validación

Implementa validación antes de clonar:

```python
class ValidatedJobConfig(IPrototypeJob):
    def __init__(self, name: str, retries: int, timeout: int, metadata: dict):
        self._validate(name, retries, timeout, metadata)
        # ... resto de la inicialización
    
    def _validate(self, name: str, retries: int, timeout: int, metadata: dict):
        """Valida que los parámetros sean correctos"""
        # TODO: Implementar validaciones
        # - name no debe estar vacío
        # - retries debe ser >= 0 y <= 10
        # - timeout debe ser > 0
        # - metadata debe contener "priority"
        pass
    
    def clone(self) -> "ValidatedJobConfig":
        """Clone que también valida"""
        # TODO: Implementar
        pass
```

## Clonación Manual vs Automática

### Clonación Automática (usando deepcopy)

```python
def clone(self) -> "JobConfig":
    return copy.deepcopy(self)
```

**Ventajas:**
- Simple y conciso
- Maneja objetos anidados automáticamente
- Maneja referencias circulares

**Desventajas:**
-  Puede ser lento para objetos grandes
-  No funciona con todos los tipos (sockets, archivos, etc.)

### Clonación Manual

```python
def clone(self) -> "JobConfig":
    return JobConfig(
        name=self._name,
        retries=self._retries,
        timeout=self._timeout,
        metadata=copy.deepcopy(self.metadata)
    )
```

**Ventajas:**
- Control fino sobre qué se clona
- Puede ser más eficiente
- Funciona con tipos personalizados

**Desventajas:**
- Más código
- Hay que actualizar cuando cambia la clase

## Conclusiones Clave

1. **Eficiencia**: Clonar es más rápido que crear desde cero cuando los objetos son complejos
2. **Reutilización**: Los prototipos permiten configuraciones base reutilizables
3. **Independencia**: Deep copy garantiza que las copias sean totalmente independientes
4. **Registry**: El patrón Registry complementa perfectamente al Prototype
5. **Flexibilidad**: Agrega, modifica o elimina prototipos en tiempo de ejecución

## Próximos Pasos

- Implementa el patrón Prototype en tu propio proyecto
- Experimenta con shallow copy vs deep copy
- Combina Prototype con otros patrones (Factory, Builder)
- Estudia el patrón Memento para comparar (también usa clonación)

## Preguntas para Reflexionar

1. ¿Cuándo preferirías Factory Method sobre Prototype?
2. ¿Cómo manejarías objetos que no pueden ser copiados (sockets, archivos)?
3. ¿Qué estrategia usarías para validar prototipos antes de registrarlos?
4. ¿Cómo implementarías un sistema de herencia entre prototipos?

---

**¡Felicidades!** Ahora dominas el patrón Prototype y puedes crear sistemas eficientes de clonación de objetos.
