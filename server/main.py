from http.server import BaseHTTPRequestHandler
import re
from typing import Callable

from common.http_statuses import HttpMethodsType

from routes import routes


class CustomHttpRequestHandler(BaseHTTPRequestHandler):
    methods: tuple[HttpMethodsType, ...] = (
        'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE',
    )

    @staticmethod
    def add_routes(method: HttpMethodsType) -> Callable:
        def outer(_: Callable[[BaseHTTPRequestHandler], None]) -> Callable:
            def inner(request: BaseHTTPRequestHandler) -> None:
                for path, handler in routes.get(method, {}).items():
                    real_path = request.path.split('?')[0].rstrip('/')
                    if bool(re.match(rf'^{path.rstrip('/')}$', real_path)):
                        return handler(request)
            return inner
        return outer


for method in CustomHttpRequestHandler.methods:
    setattr(
        CustomHttpRequestHandler,
        f'do_{method}',
        CustomHttpRequestHandler.add_routes(method)(lambda _: _)
    )


__all__ = ('CustomHttpRequestHandler',)
