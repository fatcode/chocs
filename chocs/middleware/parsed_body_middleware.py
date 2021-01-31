import inspect
from typing import Any

from chocs.http_request import HttpRequest
from chocs.http_response import HttpResponse
from chocs.middleware import Middleware, MiddlewareHandler
from chocs.routing import Route


class ParsedBodyMiddleware(Middleware):
    def __init__(self, strict: bool = True):
        self.strict = strict

    def handle(self, request: HttpRequest, next: MiddlewareHandler) -> HttpResponse:
        route = request.route
        if "parsed_body" in route.attributes:
            self._map_parsed_body(request, route)

        return next(request)

    def _map_parsed_body(self, request: HttpRequest, route: Route) -> None:
        if not inspect.isclass(route.attributes["parsed_body"]):
            return

        body = request.parsed_body

        strict = route.attributes["strict"] if "strict" in route.attributes else self.strict
        constructor = route.attributes["parsed_body"]
        request._parsed_body = None

        if not strict:

            def _get_non_strict_parsed_body() -> Any:

                instance = constructor.__new__(constructor)
                for prop_name, prop_value in body.items():
                    setattr(instance, prop_name, prop_value)

                if hasattr(instance, "__post_init__"):
                    instance.__post_init__()

                return instance

            request._parsed_body_getter = _get_non_strict_parsed_body

            return

        def _get_strict_parsed_body() -> Any:
            return constructor(**body)

        request._parsed_body_getter = _get_strict_parsed_body


__all__ = ["ParsedBodyMiddleware"]
