from creational_patterns.builder.builder_http_request import IBuilderHttpRequest


class BuilderDirector:
    _builder: IBuilderHttpRequest

    def __init__(self, builder: IBuilderHttpRequest):
        self._builder = builder
    
    def change_builder(self, builder: IBuilderHttpRequest):
        self._builder = builder
    
    def build_get_request(self):
        self._builder.reset()
        self._builder.set_url("https://example.com")
        self._builder.set_method("GET")
        self._builder.set_timeout(10)
    
    def build_post_request(self):
        self._builder.reset()
        self._builder.set_url("https://example.com")
        self._builder.set_method("POST")
        self._builder.set_body({"key": "value"})
        self._builder.set_timeout(10)
        self._builder.add_header("Authorization", "Bearer 1234567890")

    def build_put_request(self):
        self._builder.reset()
        self._builder.set_url("https://example.com")
        self._builder.set_method("PUT")
        self._builder.set_body({"key": "value"})
        self._builder.set_timeout(10)
        self._builder.add_header("Authorization", "Bearer 1234567890")
