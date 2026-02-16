from creational_patterns.abstract_factory.provider_factory import IProviderFactory


class NotificationService:
    def __init__(self, factory: IProviderFactory):
        self.email_sender = factory.create_email_sender()
        self.sms_sender = factory.create_sms_sender()
    
    def send_notification(self, email: str, sms: str, message: str) -> None:
        self.email_sender.send(email, message)
        self.sms_sender.send(sms, message)
