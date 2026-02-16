from creational_patterns.abstract_factory.sms_sender import ISmsSender


class TwilioSmsSender(ISmsSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando SMS via Twilio a {to}... mensaje: {message}")
