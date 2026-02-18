# Patrón Prototype (Prototipo)

## Descripción

El patrón **Prototype** es un patrón de diseño creacional que permite copiar objetos existentes sin que el código dependa de sus clases. Este patrón delega el proceso de clonación a los propios objetos que están siendo clonados.

## Propósito

- Crear nuevos objetos clonando instancias existentes (prototipos)
- Evitar la creación costosa de objetos desde cero
- Reducir el número de subclases necesarias
- Ocultar la complejidad de crear instancias al cliente

## Implementación en este Proyecto

Este ejemplo implementa un **Sistema de Plantillas de Configuración de Jobs** donde se pueden registrar configuraciones predefinidas (prototipos) y crear nuevas instancias mediante clonación. Esto es especialmente útil cuando crear un objeto desde cero es costoso o complejo.

### Estructura del Proyecto

```
prototype/
├── prototype_job.py     # Interfaz del Prototype
├── config.py           # Implementación concreta (JobConfig)
├── templates.py        # Registro de prototipos (JobTemplates)
└── main.py            # Ejemplos de uso
```

### Componentes Principales

#### 1. Interfaz Prototype
- **`IPrototypeJob`**: Define el contrato para objetos clonables
  - `clone()` - Método para crear una copia del objeto

#### 2. Prototype Concreto
- **`JobConfig`**: Configuración de un Job que puede clonarse
  - Atributos: nombre, reintentos, timeout, metadata
  - Implementa `clone()` usando `copy.deepcopy()`

#### 3. Registro de Prototipos
- **`JobTemplates`**: Almacena y gestiona prototipos predefinidos
  - `register(key, template)` - Registra un prototipo
  - `get(key)` - Obtiene una copia del prototipo

## Ventajas

- **Eficiencia**: Clonar objetos puede ser más rápido que crearlos desde cero
- **Simplicidad**: Evita subclases complejas de objetos factory
- **Flexibilidad**: Agrega y elimina prototipos en tiempo de ejecución
- **Configuraciones Predefinidas**: Mantén templates listos para usar
- **Independencia**: El cliente no necesita conocer las clases concretas
- **Objetos Complejos**: Ideal para objetos con muchos campos o inicialización costosa

## Uso Básico

### Registrar Prototipos

```python
from creational_patterns.prototype.config import JobConfig
from creational_patterns.prototype.templates import JobTemplates

# Registrar un template "fast"
JobTemplates.register(
    "fast",
    JobConfig(
        name="fast-job",
        retries=1,
        timeout=5,
        metadata={"priority": "high"}
    )
)

# Registrar un template "safe"
JobTemplates.register(
    "safe",
    JobConfig(
        name="safe-job",
        retries=5,
        timeout=30,
        metadata={"priority": "low"}
    )
)
```

### Obtener Copias de Prototipos

```python
# Obtener copias independientes del template "fast"
job1 = JobTemplates.get("fast")
job2 = JobTemplates.get("fast")

# Las copias son independientes
job2.metadata["priority"] = "critical"

print(job1)  # priority: "high"
print(job2)  # priority: "critical"
```

## 🎓 Cuándo Usar este Patrón

### ✔️ Usar Prototype Cuando:

1. **Creación Costosa**: La creación del objeto es costosa (I/O, base de datos, cálculos complejos)
   ```python
   # Costoso: conectar a BD, cargar configuración, etc.
   config = load_config_from_database()
   
   # Eficiente: clonar el config existente
   new_config = config.clone()
   ```

2. **Configuraciones Predefinidas**: Tienes configuraciones base que quieres reutilizar
   ```python
   dev_config = JobTemplates.get("development")
   prod_config = JobTemplates.get("production")
   ```

3. **Objetos Similares**: Necesitas muchos objetos con pequeñas variaciones
   ```python
   base_job = JobTemplates.get("standard")
   job_a = base_job.clone()
   job_a.metadata["task"] = "task_a"
   ```

4. **Evitar Jerarquía de Clases**: Quieres evitar una jerarquía compleja de factories
   ```python
   # Sin Prototype: necesitarías FastJobFactory, SafeJobFactory, etc.
   # Con Prototype: solo registra templates
   ```

### No Usar Prototype Cuando:

1. Los objetos son simples y baratos de crear
2. No hay configuraciones predefinidas que reutilizar
3. Los objetos no tienen estado complejo
4. Clonar es más complejo que crear desde cero

## Comparación con Otros Patrones

| Aspecto | Prototype | Factory Method | Builder |
|---------|-----------|----------------|---------|
| **Propósito** | Clonar objetos existentes | Crear objetos nuevos | Construir objetos paso a paso |
| **Mecanismo** | Clonación | Instanciación | Construcción incremental |
| **Cuándo usar** | Objetos costosos/complejos | Polimorfismo de creación | Muchas configuraciones |
| **Flexibilidad** | Alta (runtime) | Media | Alta |
| **Complejidad** | Baja | Baja | Media-Alta |

## Conceptos Clave

### Shallow Copy vs Deep Copy

```python
import copy

# Shallow Copy: copia el objeto pero comparte referencias
shallow = copy.copy(original)

# Deep Copy: copia el objeto y todos sus objetos anidados
deep = copy.deepcopy(original)  # ✅ Usado en este ejemplo
```

**En este proyecto usamos `deepcopy`** para garantizar que los metadatos (diccionarios anidados) sean completamente independientes.

### Registro de Prototipos

El patrón incluye típicamente un **Registro** (Registry) que:
- Almacena prototipos predefinidos
- Proporciona acceso centralizado
- Retorna copias, no el original

```python
class JobTemplates:
    _templates: Dict[str, JobConfig] = {}
    
    @classmethod
    def register(cls, key: str, template: JobConfig) -> None:
        cls._templates[key] = template
    
    @classmethod
    def get(cls, key: str) -> JobConfig:
        return cls._templates[key].clone()  # ¡Retorna una copia!
```

## Diagrama de Flujo

```
┌─────────────────┐
│    Cliente      │
└────────┬────────┘
         │
         │ usa
         ▼
┌─────────────────────┐
│  JobTemplates       │
│  (Registro)         │
│ ─────────────────── │
│ + register()        │
│ + get() → clone()   │
└────────┬────────────┘
         │
         │ almacena
         ▼
┌─────────────────────┐
│  IPrototypeJob      │ ◄── Interfaz
│  (Interfaz)         │
│ ─────────────────── │
│ + clone()           │
└────────┬────────────┘
         │
         │ implementa
         ▼
┌─────────────────────┐
│    JobConfig        │
│    (Prototipo)      │
│ ─────────────────── │
│ + clone()           │
│   return deepcopy() │
└─────────────────────┘
```

## Casos de Uso Reales

### 1. Configuración de Entornos
```python
# Template base para desarrollo
dev_template = JobConfig(name="dev", retries=1, timeout=10, metadata={...})

# Cada desarrollador clona y personaliza
jorge_config = dev_template.clone()
jorge_config.metadata["user"] = "jorge"

maria_config = dev_template.clone()
maria_config.metadata["user"] = "maria"
```

### 2. Sistema de Documentos
```python
# Templates de documentos
DocumentTemplates.register("invoice", InvoiceTemplate())
DocumentTemplates.register("report", ReportTemplate())

# Crear documentos basados en templates
invoice1 = DocumentTemplates.get("invoice")
invoice1.customer = "Cliente A"

invoice2 = DocumentTemplates.get("invoice")
invoice2.customer = "Cliente B"
```

### 3. Configuración de Juegos
```python
# Perfiles de personajes
CharacterTemplates.register("warrior", Warrior(hp=100, attack=20))
CharacterTemplates.register("mage", Mage(hp=50, magic=40))

# Crear personajes basados en templates
player1 = CharacterTemplates.get("warrior")
player2 = CharacterTemplates.get("mage")
```

## Ejecutar el Ejemplo

```bash
cd /home/jorge/Documents/projects/design-patterns
python -m creational_patterns.prototype.main
```

## Salida Esperada

```
JobConfig(name='fast-job', retries=1, timeout=5, metadata={'priority': 'high'})
JobConfig(name='fast-job', retries=1, timeout=5, metadata={'priority': 'critical'})
JobConfig(name='safe-job', retries=5, timeout=30, metadata={'priority': 'low'})
```

**Nota**: Observa que `job1` mantiene `priority: 'high'` mientras que `job2` tiene `priority: 'critical'`, demostrando que son copias independientes.

## Consideraciones Importantes

### 1. Deep Copy vs Shallow Copy

```python
# Shallow copy - comparte referencias
def clone_shallow(self):
    return copy.copy(self)  # ¡metadata se comparte!

# Deep copy - copias independientes
def clone_deep(self):
    return copy.deepcopy(self)  # metadata es independiente
```

### 2. Objetos No Serializables

Algunos objetos no pueden ser copiados con `deepcopy` (sockets, archivos abiertos, etc.):

```python
def clone(self):
    # Clonar manualmente campos específicos
    new_obj = JobConfig(
        name=self._name,
        retries=self._retries,
        timeout=self._timeout,
        metadata=copy.deepcopy(self.metadata)
    )
    return new_obj
```

### 3. Referencias Circulares

`deepcopy` maneja referencias circulares automáticamente, pero ten cuidado con objetos muy anidados.

## Referencias

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns) (Gang of Four)
- [Refactoring Guru - Prototype Pattern](https://refactoring.guru/design-patterns/prototype)
- [Python copy module documentation](https://docs.python.org/3/library/copy.html)

## Ver También

- [TUTORIAL.md](./TUTORIAL.md) - Tutorial paso a paso con ejemplos detallados
- [Factory Method Pattern](../factory_method/) - Alternativa para crear objetos
- [Builder Pattern](../builder/) - Para construcción compleja paso a paso
