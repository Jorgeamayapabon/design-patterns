from creational_patterns.abstract_factory.email_aws import AwsEmailSender
from creational_patterns.abstract_factory.email_sender import IEmailSender
from creational_patterns.abstract_factory.provider_factory import IProviderFactory
from creational_patterns.abstract_factory.sms_aws import AwsSmsSender
from creational_patterns.abstract_factory.sms_sender import ISmsSender


class AwsFactory(IProviderFactory):
    def create_email_sender(self) -> IEmailSender:
        return AwsEmailSender()

    def create_sms_sender(self) -> ISmsSender:
        return AwsSmsSender()
