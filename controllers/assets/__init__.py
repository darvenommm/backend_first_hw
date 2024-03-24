from os import getcwd

from http.server import BaseHTTPRequestHandler as HTTPRequest


class AssetsController:
    @staticmethod
    def get_styles(request: HTTPRequest) -> None:
        request.send_response(200)
        request.send_header('Content-Type', 'text/css')
        request.end_headers()

        with open(f'{getcwd()}/views/styles/styles.css') as file:
            request.wfile.write(file.read().encode())


__all__ = ('AssetsController',)
