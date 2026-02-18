from creational_patterns.builder.builder_http_request import IBuilderHttpRequest
from creational_patterns.builder.http_request import HttpRequest


class BuilderConcreteHttpRequest(IBuilderHttpRequest):
    _request: HttpRequest
    _headers: dict

    def reset(self) -> None:
        self._request = HttpRequest()
        self._headers = {}

    def set_url(self, url: str) -> None:
        self._request.set_url(url)

    def set_method(self, method: str) -> None:
        self._request.set_method(method)

    def set_body(self, body: dict) -> None:
        self._request.set_body(body)
    
    def set_timeout(self, timeout: int) -> None:
        self._request.set_timeout(timeout)

    def add_header(self, key: str, value: str) -> None:
        self._headers[key] = value
        self._request.set_headers(self._headers)
    
    def get_request(self) -> HttpRequest:
        return self._request
