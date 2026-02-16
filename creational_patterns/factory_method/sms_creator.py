from creational_patterns.factory_method.notification import INotification
from creational_patterns.factory_method.notification_creator import NotificationCreator
from creational_patterns.factory_method.sms_notification import SmsNotification


class SmsCreator(NotificationCreator):
    def create_notification(self) -> INotification:
        return SmsNotification()
