from creational_patterns.factory_method.email_creator import EmailCreator
from creational_patterns.factory_method.sms_creator import SmsCreator
from creational_patterns.factory_method.whatsapp_creator import WhatsappCreator


def send_email_notification():
    sender = EmailCreator()
    sender.send_notification("Hello, world!")


def send_sms_notification():
    sender = SmsCreator()
    sender.send_notification("Hello, world!")


def send_whatsapp_notification():
    sender = WhatsappCreator()
    sender.send_notification("Hello, world!")


def main():
    send_email_notification()
    send_sms_notification()
    send_whatsapp_notification()


if __name__ == "__main__":
    main()
