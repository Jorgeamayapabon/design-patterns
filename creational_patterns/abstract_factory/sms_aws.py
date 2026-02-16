from creational_patterns.abstract_factory.sms_sender import ISmsSender


class AwsSmsSender(ISmsSender):
    def send(self, to: str, message: str) -> None:
        print(f"Enviando SMS via AWS a {to}... mensaje: {message}")
