from abc import ABC, abstractmethod

from creational_patterns.factory_method.notification import INotification


class NotificationCreator(ABC):

    @abstractmethod
    def create_notification(self) -> INotification:
        pass

    def send_notification(self, message: str) -> None:
        notification: INotification = self.create_notification()
        notification.send(message)
