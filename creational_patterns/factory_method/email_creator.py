from creational_patterns.factory_method.email_notification import EmailNotification
from creational_patterns.factory_method.notification import INotification
from creational_patterns.factory_method.notification_creator import NotificationCreator


class EmailCreator(NotificationCreator):
    def create_notification(self) -> INotification:
        return EmailNotification()
