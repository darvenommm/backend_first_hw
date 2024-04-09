from http.server import BaseHTTPRequestHandler

from routes import Router


@Router.set_routes
class CustomHttpRequestHandler(BaseHTTPRequestHandler):
    pass


__all__ = ('CustomHttpRequestHandler',)
