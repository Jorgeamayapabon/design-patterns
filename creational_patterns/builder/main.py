from creational_patterns.builder.builder_concrete_http_request import BuilderConcreteHttpRequest
from creational_patterns.builder.builder_director import BuilderDirector
from creational_patterns.builder.http_request import HttpRequest


def run():
    builder: BuilderConcreteHttpRequest = BuilderConcreteHttpRequest()
    director: BuilderDirector = BuilderDirector(builder)

    director.build_get_request()
    get_request: HttpRequest = builder.get_request()
    print(get_request)

    director.build_post_request()
    post_request: HttpRequest = builder.get_request()
    print(post_request)

    director.build_put_request()
    put_request: HttpRequest = builder.get_request()
    print(put_request)

    # Caso de uso sin director
    builder.reset()
    builder.set_url("https://example.com")
    builder.set_method("GET")
    builder.set_timeout(10)
    builder.add_header("Authorization", "Bearer 1234567890")
    get_request: HttpRequest = builder.get_request()
    print(get_request)


if __name__ == "__main__":
    run()
