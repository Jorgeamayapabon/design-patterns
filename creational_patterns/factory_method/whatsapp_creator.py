from creational_patterns.factory_method.notification import INotification
from creational_patterns.factory_method.notification_creator import NotificationCreator
from creational_patterns.factory_method.whatsapp_notification import WhatsappNotification


class WhatsappCreator(NotificationCreator):
    def create_notification(self) -> INotification:
        return WhatsappNotification()
