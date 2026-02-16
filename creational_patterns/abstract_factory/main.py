from creational_patterns.abstract_factory.aws_factory import AwsFactory
from creational_patterns.abstract_factory.notification_service import NotificationService
from creational_patterns.abstract_factory.twilio_factory import TwilioFactory


def send_twilio():
    factory = TwilioFactory()
    service = NotificationService(factory)
    service.send_notification("test@test.com", "1234567890", "Hello, world!")


def send_aws():
    factory = AwsFactory()
    service = NotificationService(factory)
    service.send_notification("test@test.com", "1234567890", "Hello, world!")


def main():
    send_twilio()
    send_aws()


if __name__ == "__main__":
    main()
