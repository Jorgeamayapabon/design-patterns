class HttpRequest:
    _url: str
    _method: str
    _headers: dict = {}
    _body: dict = {}
    _timeout: int

    def set_url(self, url: str):
        self._url = url
    
    def set_method(self, method: str):
        self._method = method
    
    def set_headers(self, headers: dict):
        self._headers = headers
    
    def set_body(self, body: dict):
        self._body = body
    
    def set_timeout(self, timeout: int):
        self._timeout = timeout

    def __repr__(self) -> str:
        return f"HttpRequest(url={self._url}, method={self._method}, headers={self._headers}, body={self._body}, timeout={self._timeout})"
