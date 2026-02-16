# Patrón Abstract Factory (Fábrica Abstracta)

## Descripción

El patrón **Abstract Factory** proporciona una interfaz para crear familias de objetos relacionados o dependientes sin especificar sus clases concretas. Este patrón es especialmente útil cuando el sistema necesita ser independiente de cómo se crean, componen y representan sus productos.

## Propósito

- Proporcionar una interfaz para crear familias de objetos relacionados
- Aislar al cliente de las clases concretas
- Facilitar el intercambio de familias de productos
- Promover la consistencia entre productos relacionados

## Implementación en este Proyecto

Este ejemplo implementa un **Sistema de Notificaciones** que puede usar diferentes proveedores (AWS o Twilio) para enviar emails y SMS. La implementación garantiza que cuando se elige un proveedor, todos los servicios relacionados (email y SMS) provengan del mismo proveedor.

### Estructura del Proyecto

```
abstract_factory/
├── provider_factory.py      # Interfaz de la fábrica abstracta
├── email_sender.py          # Interfaz para envío de emails
├── sms_sender.py            # Interfaz para envío de SMS
├── aws_factory.py           # Fábrica concreta de AWS
├── twilio_factory.py        # Fábrica concreta de Twilio
├── email_aws.py             # Implementación de email con AWS
├── sms_aws.py               # Implementación de SMS con AWS
├── twilio_email.py          # Implementación de email con Twilio
├── sms_twilio.py            # Implementación de SMS con Twilio
├── notification_service.py  # Cliente que usa la fábrica
└── main.py                  # Punto de entrada con ejemplos
```

### Componentes Principales

#### 1. Productos Abstractos
- **`IEmailSender`**: Interfaz para servicios de envío de email
- **`ISmsSender`**: Interfaz para servicios de envío de SMS

#### 2. Fábrica Abstracta
- **`IProviderFactory`**: Define los métodos para crear productos relacionados
  - `create_email_sender()` → IEmailSender
  - `create_sms_sender()` → ISmsSender

#### 3. Fábricas Concretas
- **`AwsFactory`**: Crea productos de la familia AWS
- **`TwilioFactory`**: Crea productos de la familia Twilio

#### 4. Productos Concretos
- **Familia AWS**: `AwsEmailSender`, `AwsSmsSender`
- **Familia Twilio**: `TwilioEmailSender`, `TwilioSmsSender`

#### 5. Cliente
- **`NotificationService`**: Usa la fábrica para enviar notificaciones sin conocer las implementaciones concretas

## Ventajas

- **Consistencia**: Garantiza que se usen productos de la misma familia
- **Aislamiento**: El cliente no depende de clases concretas
- **Flexibilidad**: Fácil cambio entre familias de productos
- **Principio Open/Closed**: Nuevas familias sin modificar código existente
- **Single Responsibility**: Cada fábrica se encarga de crear su familia

## Uso Básico

```python
from creational_patterns.abstract_factory.aws_factory import AwsFactory
from creational_patterns.abstract_factory.notification_service import NotificationService

# Crear servicio con proveedor AWS
factory = AwsFactory()
service = NotificationService(factory)
service.send_notification("user@example.com", "+123456789", "¡Hola!")

# Cambiar a Twilio solo cambiando la fábrica
from creational_patterns.abstract_factory.twilio_factory import TwilioFactory
factory = TwilioFactory()
service = NotificationService(factory)
service.send_notification("user@example.com", "+123456789", "¡Hola!")
```

## Cuándo Usar este Patrón

- Cuando el sistema debe ser independiente de cómo se crean sus productos
- Cuando se necesita trabajar con múltiples familias de productos relacionados
- Cuando se quiere garantizar que los productos de una familia se usen juntos
- Cuando se desea proporcionar una biblioteca de productos sin exponer implementaciones

## Comparación con Factory Method

| Aspecto | Abstract Factory | Factory Method |
|---------|-----------------|----------------|
| **Propósito** | Crear familias de objetos relacionados | Crear un solo tipo de objeto |
| **Complejidad** | Mayor | Menor |
| **Productos** | Múltiples productos relacionados | Un solo producto |
| **Consistencia** | Garantiza productos de la misma familia | No aplica |

## Referencias

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns) (Gang of Four)
- [Refactoring Guru - Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)

## Ver También

- [TUTORIAL.md](./TUTORIAL.md) - Tutorial paso a paso para entender la implementación
- [Factory Method Pattern](../factory_method/) - Patrón relacionado más simple
