from http.server import BaseHTTPRequestHandler

from common.http import HttpMethodsType

from routes import Routes


@Routes
class CustomHttpRequestHandler(BaseHTTPRequestHandler):
    methods: tuple[HttpMethodsType, ...] = ('GET', 'POST', 'DELETE')


__all__ = ('CustomHttpRequestHandler',)
