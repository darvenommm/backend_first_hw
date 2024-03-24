from http.server import BaseHTTPRequestHandler as HTTPRequest
from typing import Any


class Request:
    @staticmethod
    def parse_queries(request: HTTPRequest) -> dict[str, Any]:
        if '?' not in request.path:
            return {}

        return {
            key: value for key, value
            in (couple.split('=') for couple in request.path.split('?')[1].split('&'))
        }
