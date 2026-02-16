from creational_patterns.abstract_factory.email_sender import IEmailSender
from creational_patterns.abstract_factory.provider_factory import IProviderFactory
from creational_patterns.abstract_factory.sms_sender import ISmsSender
from creational_patterns.abstract_factory.sms_twilio import TwilioSmsSender
from creational_patterns.abstract_factory.twilio_email import TwilioEmailSender


class TwilioFactory(IProviderFactory):
    def create_email_sender(self) -> IEmailSender:
        return TwilioEmailSender()

    def create_sms_sender(self) -> ISmsSender:
        return TwilioSmsSender()
