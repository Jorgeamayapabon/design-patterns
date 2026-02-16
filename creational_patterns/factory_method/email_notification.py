from creational_patterns.factory_method.notification import INotification


class EmailNotification(INotification):
    def send(self, message: str) -> None:
        print(f"Enviando notificacion via email... mensaje: {message}")
