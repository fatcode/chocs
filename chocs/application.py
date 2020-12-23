from functools import cached_property
from typing import Callable, Optional, Union

from .http_method import HttpMethod
from .http_request import HttpRequest
from .http_response import HttpResponse
from .middleware import Middleware, MiddlewarePipeline
from .router_middleware import RouterMiddleware
from .routing import Route, Router
from .serverless.wrapper import create_serverless_function


class Application:
    def __init__(self, *middleware: Union[Middleware, Callable]):
        self.parent: Optional[Application] = None
        self._middleware = MiddlewarePipeline()
        for item in middleware:
            self._middleware.append(item)

        self.namespace = ["/"]
        self.router = Router()

    def _append_route(
        self,
        method: HttpMethod,
        route: Route,
        handler: Callable[[HttpRequest], HttpResponse],
    ):
        if self.parent:
            self.parent._append_route(method, route, handler)

        self.router.append(route, handler, method)

    def _create_route(self, route: str) -> Route:
        base_uri = "".join(self.namespace[1:])
        return Route(base_uri + route)

    def get(self, route: str) -> Callable:
        def _get(handler: Callable) -> Callable:
            r = self._create_route(route)
            self._append_route(HttpMethod.GET, r, handler)
            return create_serverless_function(handler, r, self._middleware)

        return _get

    def post(self, route: str) -> Callable:
        def _post(handler: Callable) -> Callable:
            r = self._create_route(route)
            self._append_route(HttpMethod.POST, r, handler)
            return create_serverless_function(handler, r, self._middleware)

        return _post

    def put(self, route: str) -> Callable:
        def _put(handler: Callable) -> Callable:
            r = self._create_route(route)
            self._append_route(HttpMethod.PUT, r, handler)
            return create_serverless_function(handler, r, self._middleware)

        return _put

    def patch(self, route: str) -> Callable:
        def _patch(handler: Callable) -> Callable:
            r = self._create_route(route)
            self._append_route(HttpMethod.PATCH, r, handler)
            return create_serverless_function(handler, r, self._middleware)

        return _patch

    def delete(self, route: str) -> Callable:
        def _delete(handler: Callable) -> Callable:
            r = self._create_route(route)
            self._append_route(HttpMethod.DELETE, r, handler)
            return create_serverless_function(handler, r, self._middleware)

        return _delete

    def head(self, route: str) -> Callable:
        def _head(handler: Callable) -> Callable:
            r = self._create_route(route)
            self._append_route(HttpMethod.HEAD, r, handler)
            return create_serverless_function(handler, r, self._middleware)

        return _head

    def options(self, route: str) -> Callable:
        def _options(handler: Callable) -> Callable:
            r = self._create_route(route)
            self._append_route(HttpMethod.OPTIONS, r, handler)
            return create_serverless_function(handler, r, self._middleware)

        return _options

    def any(self, route: str) -> Callable:
        def _any(handler: Callable) -> Callable:
            r = self._create_route(route)
            self._append_route(HttpMethod.GET, r, handler)
            self._append_route(HttpMethod.POST, r, handler)
            self._append_route(HttpMethod.PUT, r, handler)
            self._append_route(HttpMethod.PATCH, r, handler)
            self._append_route(HttpMethod.DELETE, r, handler)
            self._append_route(HttpMethod.HEAD, r, handler)
            self._append_route(HttpMethod.OPTIONS, r, handler)

            return create_serverless_function(handler, r, self._middleware)

        return _any

    def group(self, base_route: str) -> "Application":
        self.namespace.append(base_route)
        return self

    def __enter__(self) -> "Application":
        child_app = Application()
        child_app._middleware = self._middleware
        child_app.namespace = self.namespace
        child_app.parent = self

        return child_app

    def __exit__(self, *args) -> "Application":
        self.namespace.pop()
        return self

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self._application_middleware(request)

    @cached_property
    def _application_middleware(self) -> MiddlewarePipeline:
        middleware = MiddlewarePipeline(self._middleware.queue)
        middleware.append(RouterMiddleware(self.router))

        return middleware


__all__ = ["Application"]
