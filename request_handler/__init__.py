from http.server import BaseHTTPRequestHandler
import re
from typing import Callable

from routes import routes


class CustomHttpRequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def add_routes(method: str) -> Callable:
        def outer(_: Callable[[BaseHTTPRequestHandler], None]) -> Callable:
            def inner(request: BaseHTTPRequestHandler) -> None:
                for path, handler in routes.get(method.upper(), {}).items():
                    request_path = request.path.split('?')[0]
                    request_path = request_path.rstrip() if request_path != '/' else request_path
                    if bool(re.match(path, request_path)):
                        return handler(request)
            return inner
        return outer

    @add_routes('GET')
    def do_GET(self) -> None:
        pass

    @add_routes('POST')
    def do_POST(self) -> None:
        pass

    @add_routes('PUT')
    def do_PUT(self) -> None:
        pass

    @add_routes('DELETE')
    def do_DELETE(self) -> None:
        pass

    @add_routes('HEAD')
    def do_HEAD(self) -> None:
        pass


__all__ = ('CustomHttpRequestHandler',)
