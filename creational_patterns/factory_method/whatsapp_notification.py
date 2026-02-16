from creational_patterns.factory_method.notification import INotification


class WhatsappNotification(INotification):
    def send(self, message: str) -> None:
        print(f"Enviando notificacion via Whatsapp... mensaje: {message}")
