# Tutorial: Factory Method Pattern

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Problema que Resuelve](#problema-que-resuelve)
3. [Anatomía del Patrón](#anatomía-del-patrón)
4. [Implementación Paso a Paso](#implementación-paso-a-paso)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Comparación con Otros Patrones](#comparación-con-otros-patrones)
7. [Ejercicios Propuestos](#ejercicios-propuestos)

---

## Introducción

El **Factory Method** es un patrón de diseño creacional que resuelve el problema de crear objetos sin especificar sus clases concretas. Define una interfaz para crear objetos, pero permite que las subclases decidan qué clase instanciar.

### Concepto Clave

> "No llames a `new`, llama a un método que decidirá qué crear"

En lugar de:
```python
notificacion = EmailNotification()  # Acoplamiento directo
```

Usamos:
```python
creator = EmailCreator()            # Trabajamos con abstracciones
notificacion = creator.create_notification()
```

---

## Problema que Resuelve

### Escenario sin Factory Method

Imagina que tienes una aplicación que envía notificaciones por email:

```python
class NotificationService:
    def send_notification(self, message: str):
        email = EmailNotification()
        email.send(message)
```

**Problemas:**
1. **Acoplamiento fuerte**: El código está atado a `EmailNotification`
2. **Difícil de extender**: Para agregar SMS, hay que modificar la clase existente
3. **Viola Open/Closed**: No está abierto a extensión, pero cerrado a modificación
4. **Difícil de testear**: No puedes inyectar mocks fácilmente

### Escenario con Factory Method

```python
class NotificationService:
    def __init__(self, creator: NotificationCreator):
        self.creator = creator
    
    def send_notification(self, message: str):
        notification = self.creator.create_notification()
        notification.send(message)

# Uso
service = NotificationService(EmailCreator())
service.send_notification("¡Hola!")

# Fácil cambiar a SMS sin modificar NotificationService
service = NotificationService(SmsCreator())
service.send_notification("¡Hola!")
```

**Ventajas:**
1. **Bajo acoplamiento**: Trabaja con abstracciones
2. **Fácil de extender**: Solo agrega nuevos creators
3. **Cumple Open/Closed**: Extensible sin modificación
4. **Testeable**: Inyecta mocks fácilmente

---

## Anatomía del Patrón

El Factory Method consta de **4 componentes principales**:

### 1. Product Interface (INotification)

Define el contrato que todos los productos deben cumplir.

```python
from abc import ABC, abstractmethod

class INotification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        """Envía una notificación con el mensaje dado"""
        pass
```

**Responsabilidad**: Establecer la interfaz común para todos los productos.

### 2. Concrete Products (EmailNotification, SmsNotification, etc.)

Implementaciones específicas del producto.

```python
class EmailNotification(INotification):
    def send(self, message: str) -> None:
        print(f"📧 Enviando email: {message}")

class SmsNotification(INotification):
    def send(self, message: str) -> None:
        print(f"📱 Enviando SMS: {message}")

class WhatsappNotification(INotification):
    def send(self, message: str) -> None:
        print(f"💬 Enviando WhatsApp: {message}")
```

**Responsabilidad**: Implementar el comportamiento específico de cada tipo de notificación.

### 3. Creator Abstract Class (NotificationCreator)

Define el factory method y la lógica de negocio que lo utiliza.

```python
from abc import ABC, abstractmethod

class NotificationCreator(ABC):
    
    @abstractmethod
    def create_notification(self) -> INotification:
        """Factory Method: Las subclases deciden qué crear"""
        pass
    
    def send_notification(self, message: str) -> None:
        """Lógica de negocio que usa el factory method"""
        # Llamamos al factory method (implementado por subclases)
        notification = self.create_notification()
        
        # Usamos el producto creado
        notification.send(message)
```

**Aspectos clave:**
- El método `create_notification()` es **abstracto** (factory method)
- El método `send_notification()` es **concreto** (lógica de negocio)
- La lógica de negocio **no sabe** qué tipo concreto de notificación se creará

### 4. Concrete Creators (EmailCreator, SmsCreator, etc.)

Implementan el factory method para crear productos específicos.

```python
class EmailCreator(NotificationCreator):
    def create_notification(self) -> INotification:
        return EmailNotification()

class SmsCreator(NotificationCreator):
    def create_notification(self) -> INotification:
        return SmsNotification()

class WhatsappCreator(NotificationCreator):
    def create_notification(self) -> INotification:
        return WhatsappNotification()
```

**Responsabilidad**: Decidir qué clase concreta instanciar.

---

## Implementación Paso a Paso

### Paso 1: Definir la Interfaz del Producto

Primero, define qué operaciones debe soportar tu producto.

```python
# notification.py
from abc import ABC, abstractmethod

class INotification(ABC):
    """Interfaz para todas las notificaciones"""
    
    @abstractmethod
    def send(self, message: str) -> None:
        """Envía una notificación"""
        pass
```

### Paso 2: Implementar Productos Concretos

Crea las implementaciones específicas.

```python
# email_notification.py
from creational_patterns.factory_method.notification import INotification

class EmailNotification(INotification):
    def send(self, message: str) -> None:
        # Lógica específica de email
        print(f"Enviando notificacion via email... mensaje: {message}")
```

```python
# sms_notification.py
from creational_patterns.factory_method.notification import INotification

class SmsNotification(INotification):
    def send(self, message: str) -> None:
        # Lógica específica de SMS
        print(f"Enviando notificacion via SMS... mensaje: {message}")
```

### Paso 3: Definir el Creator Abstracto

El creator contiene:
- El **factory method** (abstracto)
- La **lógica de negocio** que usa el factory method (concreto)

```python
# notification_creator.py
from abc import ABC, abstractmethod
from creational_patterns.factory_method.notification import INotification

class NotificationCreator(ABC):
    
    @abstractmethod
    def create_notification(self) -> INotification:
        """
        Factory Method: Las subclases deciden qué tipo de 
        notificación crear.
        """
        pass
    
    def send_notification(self, message: str) -> None:
        """
        Lógica de negocio que usa el factory method.
        Este método NO necesita saber qué tipo de notificación
        se está creando.
        """
        # Paso 1: Crear la notificación usando el factory method
        notification: INotification = self.create_notification()
        
        # Paso 2: Usar la notificación creada
        notification.send(message)
```

### Paso 4: Implementar Creators Concretos

Cada creator decide qué producto crear.

```python
# email_creator.py
from creational_patterns.factory_method.email_notification import EmailNotification
from creational_patterns.factory_method.notification import INotification
from creational_patterns.factory_method.notification_creator import NotificationCreator

class EmailCreator(NotificationCreator):
    def create_notification(self) -> INotification:
        """Retorna una notificación de tipo Email"""
        return EmailNotification()
```

```python
# sms_creator.py
from creational_patterns.factory_method.notification import INotification
from creational_patterns.factory_method.notification_creator import NotificationCreator
from creational_patterns.factory_method.sms_notification import SmsNotification

class SmsCreator(NotificationCreator):
    def create_notification(self) -> INotification:
        """Retorna una notificación de tipo SMS"""
        return SmsNotification()
```

### Paso 5: Usar el Patrón

```python
# main.py
from creational_patterns.factory_method.email_creator import EmailCreator
from creational_patterns.factory_method.sms_creator import SmsCreator
from creational_patterns.factory_method.whatsapp_creator import WhatsappCreator

def main():
    # Crear un creator de email
    email_sender = EmailCreator()
    email_sender.send_notification("¡Bienvenido a nuestra plataforma!")
    
    # Crear un creator de SMS
    sms_sender = SmsCreator()
    sms_sender.send_notification("Tu código de verificación es: 123456")
    
    # Crear un creator de WhatsApp
    whatsapp_sender = WhatsappCreator()
    whatsapp_sender.send_notification("Tienes un nuevo mensaje")

if __name__ == "__main__":
    main()
```

---

## Ejemplos Prácticos

### Ejemplo 1: Sistema de Notificaciones Configurables

```python
def get_notification_creator(channel: str) -> NotificationCreator:
    """Factory de factories - retorna el creator apropiado"""
    creators = {
        'email': EmailCreator,
        'sms': SmsCreator,
        'whatsapp': WhatsappCreator,
    }
    
    creator_class = creators.get(channel.lower())
    if not creator_class:
        raise ValueError(f"Canal desconocido: {channel}")
    
    return creator_class()

# Uso
def send_notification_by_channel(channel: str, message: str):
    creator = get_notification_creator(channel)
    creator.send_notification(message)

# Enviar por el canal preferido del usuario
user_preference = "email"  # Esto vendría de la configuración del usuario
send_notification_by_channel(user_preference, "¡Nueva funcionalidad disponible!")
```

### Ejemplo 2: Sistema con Configuración Avanzada

```python
class AdvancedEmailCreator(NotificationCreator):
    def __init__(self, smtp_server: str, port: int):
        self.smtp_server = smtp_server
        self.port = port
    
    def create_notification(self) -> INotification:
        # Podrías pasar la configuración al producto
        return EmailNotification()
    
    def send_notification(self, message: str) -> None:
        print(f"Configurando servidor SMTP: {self.smtp_server}:{self.port}")
        super().send_notification(message)

# Uso
creator = AdvancedEmailCreator("smtp.gmail.com", 587)
creator.send_notification("Mensaje con configuración personalizada")
```

### Ejemplo 3: Sistema con Fallback

```python
class NotificationServiceWithFallback:
    def __init__(self, primary: NotificationCreator, 
                 fallback: NotificationCreator):
        self.primary = primary
        self.fallback = fallback
    
    def send_notification(self, message: str):
        try:
            self.primary.send_notification(message)
        except Exception as e:
            print(f"Error en canal primario: {e}")
            print("Usando canal de respaldo...")
            self.fallback.send_notification(message)

# Uso
service = NotificationServiceWithFallback(
    primary=EmailCreator(),
    fallback=SmsCreator()
)
service.send_notification("Mensaje importante")
```

---

## Comparación con Otros Patrones

### Factory Method vs Simple Factory

**Simple Factory** (no es un patrón GoF oficial):
```python
class NotificationFactory:
    @staticmethod
    def create_notification(type: str) -> INotification:
        if type == "email":
            return EmailNotification()
        elif type == "sms":
            return SmsNotification()
        else:
            raise ValueError("Tipo desconocido")
```

**Diferencias:**
- Simple Factory: Una única clase con lógica condicional
- Factory Method: Usa herencia, cada subclase decide qué crear
- Factory Method es más extensible (Open/Closed)

### Factory Method vs Abstract Factory

**Abstract Factory**:
- Crea **familias** de objetos relacionados
- Ejemplo: Crear `Button` y `Checkbox` en estilo Windows o Mac

**Factory Method**:
- Crea **un tipo** de objeto
- Ejemplo: Crear diferentes tipos de notificaciones

### Factory Method vs Builder

**Builder**:
- Construye objetos **paso a paso**
- Ejemplo: Construir un objeto complejo con muchos parámetros opcionales

**Factory Method**:
- Crea objetos en **una sola llamada**
- Ejemplo: Crear una notificación lista para usar

---

## Ejercicios Propuestos

### Ejercicio 1: Agregar Nuevo Tipo de Notificación

**Objetivo**: Agregar soporte para notificaciones por Telegram.

**Pasos**:
1. Crear `telegram_notification.py` que implemente `INotification`
2. Crear `telegram_creator.py` que implemente `NotificationCreator`
3. Probar en `main.py`

**Solución**:
```python
# telegram_notification.py
from creational_patterns.factory_method.notification import INotification

class TelegramNotification(INotification):
    def send(self, message: str) -> None:
        print(f"Enviando notificacion via Telegram... mensaje: {message}")

# telegram_creator.py
from creational_patterns.factory_method.notification import INotification
from creational_patterns.factory_method.notification_creator import NotificationCreator
from creational_patterns.factory_method.telegram_notification import TelegramNotification

class TelegramCreator(NotificationCreator):
    def create_notification(self) -> INotification:
        return TelegramNotification()
```

### Ejercicio 2: Sistema de Logging con Factory Method

**Objetivo**: Crear un sistema de logging que pueda escribir a diferentes destinos (Console, File, Database).

**Pistas**:
- Interface: `ILogger` con método `log(message: str, level: str)`
- Productos: `ConsoleLogger`, `FileLogger`, `DatabaseLogger`
- Creators: `ConsoleLoggerCreator`, `FileLoggerCreator`, `DatabaseLoggerCreator`

### Ejercicio 3: Sistema de Reportes

**Objetivo**: Crear un sistema que genere reportes en diferentes formatos (PDF, Excel, HTML).

**Requerimientos**:
- Interface: `IReport` con método `generate(data: dict) -> str`
- Productos: `PDFReport`, `ExcelReport`, `HTMLReport`
- Creators: `PDFReportCreator`, `ExcelReportCreator`, `HTMLReportCreator`

### Ejercicio 4: Agregar Prioridad a las Notificaciones

**Objetivo**: Extender el sistema actual para soportar prioridades (Alta, Media, Baja).

**Pistas**:
- Modificar `send_notification()` para aceptar un parámetro `priority`
- Modificar los productos para mostrar la prioridad
- Opcional: Crear creators específicos por prioridad

---

## Conclusión

El patrón Factory Method es fundamental para:

1. **Desacoplar** la creación de objetos de su uso
2. **Cumplir** el principio Open/Closed
3. **Facilitar** la extensión del sistema
4. **Mejorar** la testabilidad del código

### Cuándo NO usar Factory Method

- Cuando solo tienes un tipo de producto y no esperas más
- Cuando la creación de objetos es trivial (ej: `Person("John", 30)`)
- Cuando la complejidad adicional no aporta valor

### Mejores Prácticas

1. **Nombra claramente**: Usa sufijos como `Creator` o `Factory`
2. **Mantén simple**: No sobrecomplicar la jerarquía
3. **Documenta**: Explica qué crea cada creator
4. **Prueba**: Crea tests unitarios para cada creator

---

## Referencias

- **Gang of Four**: Design Patterns - Elements of Reusable Object-Oriented Software
- **Refactoring Guru**: https://refactoring.guru/design-patterns/factory-method
- **Source Making**: https://sourcemaking.com/design_patterns/factory_method

---

**¡Felicidades!** Has completado el tutorial de Factory Method. Ahora estás listo para aplicar este patrón en tus proyectos de producción.
