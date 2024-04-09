from http.server import BaseHTTPRequestHandler

from routes import Router


@Router.add_routing
class CustomHttpRequestHandler(BaseHTTPRequestHandler):
    pass


__all__ = ('CustomHttpRequestHandler',)
