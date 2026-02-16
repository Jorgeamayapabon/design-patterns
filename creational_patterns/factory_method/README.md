# Factory Method Pattern

## Descripción

El patrón **Factory Method** es un patrón de diseño creacional que proporciona una interfaz para crear objetos en una superclase, pero permite que las subclases alteren el tipo de objetos que se crearán.

En lugar de llamar directamente al constructor `new` para crear objetos, el patrón Factory Method delega la creación de objetos a métodos de subclases especializadas.

## Propósito

- **Desacoplar** la lógica de creación de objetos del código que los utiliza
- **Delegar** la responsabilidad de instanciación a las subclases
- **Permitir** que una clase difiera la instanciación a sus subclases
- **Facilitar** la extensión del sistema con nuevos tipos de productos sin modificar el código existente

## Estructura de la Implementación

```
factory_method/
├── notification.py              # Interface del producto (INotification)
├── notification_creator.py      # Creator abstracto (NotificationCreator)
│
├── email_notification.py        # Producto concreto: Email
├── sms_notification.py          # Producto concreto: SMS
├── whatsapp_notification.py     # Producto concreto: WhatsApp
│
├── email_creator.py             # Creator concreto: Email
├── sms_creator.py               # Creator concreto: SMS
├── whatsapp_creator.py          # Creator concreto: WhatsApp
│
└── main.py                      # Demostración de uso
```

## Componentes Principales

### 1. **INotification** (Product Interface)
Define la interfaz común para todos los productos que puede crear el factory method.

### 2. **NotificationCreator** (Creator Abstract)
- Declara el factory method `create_notification()` que debe retornar un objeto de tipo `INotification`
- Contiene la lógica de negocio `send_notification()` que utiliza el producto creado

### 3. **Concrete Creators** (EmailCreator, SmsCreator, WhatsappCreator)
- Implementan el factory method `create_notification()`
- Cada uno retorna un tipo diferente de notificación

### 4. **Concrete Products** (EmailNotification, SmsNotification, WhatsappNotification)
- Implementan la interfaz `INotification`
- Cada uno proporciona su propia implementación del método `send()`

## Caso de Uso: Sistema de Notificaciones

Esta implementación demuestra un sistema de notificaciones multi-canal donde:

- **Problema**: Una aplicación necesita enviar notificaciones por diferentes canales (Email, SMS, WhatsApp)
- **Solución**: Usar Factory Method para crear el tipo apropiado de notificación sin acoplar el código cliente a las clases concretas

## Uso Rápido

```python
from creational_patterns.factory_method.email_creator import EmailCreator
from creational_patterns.factory_method.sms_creator import SmsCreator
from creational_patterns.factory_method.whatsapp_creator import WhatsappCreator

# Crear y enviar notificación por email
email_sender = EmailCreator()
email_sender.send_notification("¡Bienvenido!")

# Crear y enviar notificación por SMS
sms_sender = SmsCreator()
sms_sender.send_notification("Código de verificación: 123456")

# Crear y enviar notificación por WhatsApp
whatsapp_sender = WhatsappCreator()
whatsapp_sender.send_notification("¡Nuevo mensaje!")
```

## Ejecución

Desde la raíz del proyecto:

```bash
python3 -m creational_patterns.factory_method.main
```

**Salida esperada:**
```
Enviando notificacion via email... mensaje: Hello, world!
Enviando notificacion via SMS... mensaje: Hello, world!
Enviando notificacion via Whatsapp... mensaje: Hello, world!
```

## Ventajas

1. **Principio Open/Closed**: Puedes agregar nuevos tipos de notificaciones sin modificar el código existente
2. **Single Responsibility**: Separas la lógica de creación de la lógica de negocio
3. **Loose Coupling**: El código cliente trabaja con abstracciones, no con clases concretas
4. **Facilita Testing**: Puedes crear mocks o stubs para testing fácilmente

## Desventajas

1. El código puede volverse más complejo con muchas subclases adicionales
2. Puede ser excesivo para casos simples donde solo hay un tipo de producto

## Cuándo Usar Factory Method

- Cuando no conoces de antemano los tipos exactos de objetos con los que tu código debe trabajar
- Cuando quieres proporcionar a los usuarios de tu biblioteca una forma de extender sus componentes internos
- Cuando quieres ahorrar recursos del sistema reutilizando objetos existentes en lugar de reconstruirlos
- Cuando la creación de objetos requiere lógica compleja que no debería estar en el constructor

## Recursos Adicionales

- Ver [TUTORIAL.md](./TUTORIAL.md) para un tutorial detallado paso a paso
- Documentación oficial de patrones de diseño: [Refactoring.Guru - Factory Method](https://refactoring.guru/design-patterns/factory-method)

## Ejemplo de Extensión

Para agregar un nuevo tipo de notificación (ej: Telegram):

1. Crear `telegram_notification.py` que implemente `INotification`
2. Crear `telegram_creator.py` que implemente `NotificationCreator`
3. No necesitas modificar ningún código existente (Open/Closed Principle)

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

---

**Nota**: Esta es una implementación didáctica con fines educativos. En un entorno de producción, las notificaciones interactuarían con APIs reales y manejarían autenticación, reintentos, logging, etc.
