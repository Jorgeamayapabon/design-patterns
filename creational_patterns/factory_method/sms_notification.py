from creational_patterns.factory_method.notification import INotification


class SmsNotification(INotification):
    def send(self, message: str) -> None:
        print(f"Enviando notificacion via SMS... mensaje: {message}")
