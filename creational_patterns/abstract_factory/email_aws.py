from creational_patterns.abstract_factory.email_sender import IEmailSender


class AwsEmailSender(IEmailSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando email via AWS a {to}... mensaje: {message}")
