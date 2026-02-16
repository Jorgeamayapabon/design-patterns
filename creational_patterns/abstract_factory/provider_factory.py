from abc import ABC, abstractmethod

from creational_patterns.abstract_factory.email_sender import IEmailSender
from creational_patterns.abstract_factory.sms_sender import ISmsSender


class IProviderFactory(ABC):
    @abstractmethod
    def create_email_sender(self) -> IEmailSender:
        pass

    @abstractmethod
    def create_sms_sender(self) -> ISmsSender:
        pass
