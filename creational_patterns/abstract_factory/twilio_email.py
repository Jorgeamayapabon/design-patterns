from creational_patterns.abstract_factory.email_sender import IEmailSender


class TwilioEmailSender(IEmailSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando email via Twilio a {to}... mensaje: {message}")
