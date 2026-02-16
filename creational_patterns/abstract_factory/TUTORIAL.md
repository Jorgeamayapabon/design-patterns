# Tutorial: Patrón Abstract Factory

## Índice

1. [Introducción](#introducción)
2. [Problema que Resuelve](#problema-que-resuelve)
3. [Solución con Abstract Factory](#solución-con-abstract-factory)
4. [Implementación Paso a Paso](#implementación-paso-a-paso)
5. [Ejecutando el Ejemplo](#ejecutando-el-ejemplo)
6. [Extendiendo el Patrón](#extendiendo-el-patrón)
7. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## Introducción

El patrón **Abstract Factory** es un patrón creacional que permite crear familias de objetos relacionados sin especificar sus clases concretas. Imagina que estás construyendo una aplicación que puede enviar notificaciones a través de diferentes proveedores (AWS, Twilio, SendGrid, etc.). Cada proveedor tiene su propia forma de enviar emails y SMS, pero quieres que tu aplicación no dependa de un proveedor específico.

## Problema que Resuelve

### Escenario Sin Abstract Factory

```python
# Cliente acoplado a implementaciones concretas
class NotificationService:
    def __init__(self, provider: str):
        if provider == "aws":
            self.email_sender = AwsEmailSender()
            self.sms_sender = AwsSmsSender()
        elif provider == "twilio":
            self.email_sender = TwilioEmailSender()
            self.sms_sender = TwilioSmsSender()
        # Problemas:
        # 1. Cliente conoce todas las implementaciones
        # 2. Agregar nuevo proveedor requiere modificar esta clase
        # 3. Posibilidad de mezclar proveedores por error
```

### Problemas Identificados

1. **Alto Acoplamiento**: El cliente depende directamente de las clases concretas
2. **Violación del Principio Open/Closed**: Agregar un nuevo proveedor requiere modificar código existente
3. **Falta de Consistencia**: Posibilidad de mezclar productos de diferentes familias por error
4. **Difícil Mantenimiento**: Cambios en los proveedores impactan al cliente

## Solución con Abstract Factory

### Diagrama Conceptual

```
┌─────────────────────┐
│  Cliente            │
│ (NotificationService)│
└──────────┬──────────┘
           │ usa
           ▼
┌─────────────────────┐
│ IProviderFactory    │ ◄─── Fábrica Abstracta
│ ─────────────────── │
│ + create_email()    │
│ + create_sms()      │
└──────────┬──────────┘
           │
           ├──────────────┬──────────────┐
           │              │              │
    ┌──────▼──────┐ ┌────▼────────┐ ┌──▼──────────┐
    │ AwsFactory  │ │TwilioFactory│ │ (Futuros)   │
    └─────────────┘ └─────────────┘ └─────────────┘
           │              │
           │              │
      crea │              │ crea
           │              │
    ┌──────▼──────┐ ┌────▼────────┐
    │AWS Products │ │Twilio Prods.│
    │─────────────│ │─────────────│
    │EmailSender  │ │ EmailSender │
    │ SmsSender   │ │ SmsSender   │
    └─────────────┘ └─────────────┘
```

## Implementación Paso a Paso

### Paso 1: Definir las Interfaces de los Productos

Primero, definimos las interfaces que todos los productos deben implementar.

**`email_sender.py`**
```python
from abc import ABC, abstractmethod

class IEmailSender(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> None:
        """Envía un email al destinatario especificado"""
        pass
```

**`sms_sender.py`**
```python
from abc import ABC, abstractmethod

class ISmsSender(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> None:
        """Envía un SMS al número especificado"""
        pass
```

**¿Por qué interfaces?** Las interfaces garantizan que todos los productos de diferentes familias tengan la misma estructura y comportamiento.

### Paso 2: Definir la Fábrica Abstracta

**`provider_factory.py`**
```python
from abc import ABC, abstractmethod
from email_sender import IEmailSender
from sms_sender import ISmsSender

class IProviderFactory(ABC):
    @abstractmethod
    def create_email_sender(self) -> IEmailSender:
        """Crea un servicio de envío de email"""
        pass
    
    @abstractmethod
    def create_sms_sender(self) -> ISmsSender:
        """Crea un servicio de envío de SMS"""
        pass
```

**Nota**: La fábrica abstracta define qué productos se pueden crear, pero no cómo se crean.

### Paso 3: Implementar Productos Concretos

Ahora implementamos los productos concretos para cada familia (proveedor).

**Familia AWS:**

**`email_aws.py`**
```python
from email_sender import IEmailSender

class AwsEmailSender(IEmailSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando email via AWS a {to}... mensaje: {message}")
        # Aquí iría la lógica real de AWS SES
```

**`sms_aws.py`**
```python
from sms_sender import ISmsSender

class AwsSmsSender(ISmsSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando SMS via AWS a {to}... mensaje: {message}")
        # Aquí iría la lógica real de AWS SNS
```

**Familia Twilio:**

**`twilio_email.py`**
```python
from email_sender import IEmailSender

class TwilioEmailSender(IEmailSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando email via Twilio a {to}... mensaje: {message}")
        # Aquí iría la lógica real de Twilio SendGrid
```

**`sms_twilio.py`**
```python
from sms_sender import ISmsSender

class TwilioSmsSender(ISmsSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando SMS via Twilio a {to}... mensaje: {message}")
        # Aquí iría la lógica real de Twilio SMS
```

### Paso 4: Implementar Fábricas Concretas

Cada fábrica concreta sabe cómo crear todos los productos de su familia.

**`aws_factory.py`**
```python
from provider_factory import IProviderFactory
from email_aws import AwsEmailSender
from sms_aws import AwsSmsSender
from email_sender import IEmailSender
from sms_sender import ISmsSender

class AwsFactory(IProviderFactory):
    def create_email_sender(self) -> IEmailSender:
        return AwsEmailSender()
    
    def create_sms_sender(self) -> ISmsSender:
        return AwsSmsSender()
```

**`twilio_factory.py`**
```python
from provider_factory import IProviderFactory
from twilio_email import TwilioEmailSender
from sms_twilio import TwilioSmsSender
from email_sender import IEmailSender
from sms_sender import ISmsSender

class TwilioFactory(IProviderFactory):
    def create_email_sender(self) -> IEmailSender:
        return TwilioEmailSender()
    
    def create_sms_sender(self) -> ISmsSender:
        return TwilioSmsSender()
```

**Punto Clave**: Cada fábrica es responsable de crear productos de UNA sola familia, garantizando consistencia.

### Paso 5: Crear el Cliente

El cliente usa la fábrica sin conocer las clases concretas.

**`notification_service.py`**
```python
from provider_factory import IProviderFactory

class NotificationService:
    def __init__(self, factory: IProviderFactory):
        # El cliente solo conoce las interfaces
        self.email_sender = factory.create_email_sender()
        self.sms_sender = factory.create_sms_sender()
    
    def send_notification(self, email: str, sms: str, message: str) -> None:
        self.email_sender.send(email, message)
        self.sms_sender.send(sms, message)
```

**¿Qué logra esto?**
- El cliente NO conoce `AwsEmailSender` ni `TwilioSmsSender`
- Solo depende de interfaces (`IEmailSender`, `ISmsSender`)
- Cambiar de proveedor es tan simple como pasar una fábrica diferente

### Paso 6: Usar el Sistema

**`main.py`**
```python
from aws_factory import AwsFactory
from twilio_factory import TwilioFactory
from notification_service import NotificationService

def main():
    # Opción 1: Usar AWS
    print("=== Usando AWS ===")
    aws_factory = AwsFactory()
    aws_service = NotificationService(aws_factory)
    aws_service.send_notification(
        "user@example.com", 
        "+1234567890", 
        "¡Bienvenido!"
    )
    
    print("\n=== Usando Twilio ===")
    # Opción 2: Usar Twilio (sin cambiar el cliente)
    twilio_factory = TwilioFactory()
    twilio_service = NotificationService(twilio_factory)
    twilio_service.send_notification(
        "user@example.com", 
        "+1234567890", 
        "¡Bienvenido!"
    )

if __name__ == "__main__":
    main()
```

## Ejecutando el Ejemplo

### 1. Navegar al directorio del proyecto

```bash
cd /home/jorge/Documents/projects/design-patterns
```

### 2. Ejecutar el ejemplo

```bash
python -m creational_patterns.abstract_factory.main
```

### 3. Salida Esperada

```
=== Usando AWS ===
Enviando email via AWS a user@example.com... mensaje: ¡Bienvenido!
Enviando SMS via AWS a +1234567890... mensaje: ¡Bienvenido!

=== Usando Twilio ===
Enviando email via Twilio a user@example.com... mensaje: ¡Bienvenido!
Enviando SMS via Twilio a +1234567890... mensaje: ¡Bienvenido!
```

## Extendiendo el Patrón

### Agregando un Nuevo Proveedor (SendGrid)

Para agregar un nuevo proveedor, seguimos estos pasos SIN modificar código existente:

**1. Crear los productos concretos:**

```python
# sendgrid_email.py
from email_sender import IEmailSender

class SendGridEmailSender(IEmailSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando email via SendGrid a {to}... mensaje: {message}")

# sendgrid_sms.py  
from sms_sender import ISmsSender

class SendGridSmsSender(ISmsSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando SMS via SendGrid a {to}... mensaje: {message}")
```

**2. Crear la fábrica concreta:**

```python
# sendgrid_factory.py
from provider_factory import IProviderFactory
from sendgrid_email import SendGridEmailSender
from sendgrid_sms import SendGridSmsSender

class SendGridFactory(IProviderFactory):
    def create_email_sender(self) -> IEmailSender:
        return SendGridEmailSender()
    
    def create_sms_sender(self) -> ISmsSender:
        return SendGridSmsSender()
```

**3. Usar el nuevo proveedor:**

```python
# En main.py
sendgrid_factory = SendGridFactory()
service = NotificationService(sendgrid_factory)
service.send_notification("user@example.com", "+1234567890", "¡Hola!")
```

**¡Sin modificar código existente!**

### Agregando un Nuevo Producto (Push Notifications)

Para agregar un nuevo tipo de producto a todas las familias:

**1. Crear la interfaz:**

```python
# push_sender.py
from abc import ABC, abstractmethod

class IPushSender(ABC):
    @abstractmethod
    def send(self, device_token: str, message: str) -> None:
        pass
```

**2. Actualizar la fábrica abstracta:**

```python
# provider_factory.py
class IProviderFactory(ABC):
    # ... métodos existentes ...
    
    @abstractmethod
    def create_push_sender(self) -> IPushSender:
        pass
```

**3. Implementar en cada familia:**

```python
# aws_push.py
class AwsPushSender(IPushSender):
    def send(self, device_token: str, message: str) -> None:
        print(f"Push via AWS SNS a {device_token}: {message}")

# En aws_factory.py
class AwsFactory(IProviderFactory):
    # ... métodos existentes ...
    
    def create_push_sender(self) -> IPushSender:
        return AwsPushSender()
```

## Ejercicios Prácticos

### Ejercicio 1: Agregar Validación

Modifica los productos para que validen los datos antes de enviar:

```python
class AwsEmailSender(IEmailSender):
    def send(self, to: str, message: str) -> None:
        if not "@" in to:
            raise ValueError("Email inválido")
        if not message:
            raise ValueError("Mensaje vacío")
        print(f"Enviando email via AWS a {to}... mensaje: {message}")
```

### Ejercicio 2: Crear un Registro de Envíos

Crea un decorador o wrapper que registre todos los envíos:

```python
class LoggingEmailSender(IEmailSender):
    def __init__(self, sender: IEmailSender):
        self._sender = sender
        self._log = []
    
    def send(self, to: str, message: str) -> None:
        self._log.append({"to": to, "message": message, "timestamp": datetime.now()})
        self._sender.send(to, message)
```

### Ejercicio 3: Implementar Factory con Configuración

Crea un sistema que elija la fábrica basándose en configuración:

```python
class FactoryProvider:
    @staticmethod
    def get_factory(config: dict) -> IProviderFactory:
        provider = config.get("provider", "aws")
        if provider == "aws":
            return AwsFactory()
        elif provider == "twilio":
            return TwilioFactory()
        else:
            raise ValueError(f"Proveedor desconocido: {provider}")

# Uso
config = {"provider": "twilio"}
factory = FactoryProvider.get_factory(config)
service = NotificationService(factory)
```

### Ejercicio 4: Agregar un Nuevo Proveedor

Implementa un proveedor completo de "Firebase" con:
- `FirebaseEmailSender`
- `FirebaseSmsSender`
- `FirebaseFactory`

## Conclusiones Clave

1. **Separación de Responsabilidades**: Cada componente tiene una responsabilidad clara
2. **Facilidad de Extensión**: Agregar nuevos proveedores o productos es sencillo
3. **Consistencia Garantizada**: Imposible mezclar productos de diferentes familias
4. **Bajo Acoplamiento**: El cliente no depende de implementaciones concretas
5. **Testabilidad**: Fácil crear mocks de las fábricas para pruebas

## Próximos Pasos

- Explora el patrón [Factory Method](../factory_method/) para comparar
- Implementa un sistema de persistencia con Abstract Factory (SQL, NoSQL, In-Memory)
- Crea un sistema de UI con diferentes temas usando este patrón

## Preguntas para Reflexionar

1. ¿Cuándo preferirías Factory Method sobre Abstract Factory?
2. ¿Cómo manejarías productos opcionales (no todas las familias los tienen)?
3. ¿Cómo implementarías una fábrica que combine productos de múltiples proveedores?

---

**¡Felicidades!** Ahora comprendes el patrón Abstract Factory y cómo aplicarlo en proyectos reales.
