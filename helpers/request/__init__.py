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

    @staticmethod
    def get_last_segment(request: HTTPRequest) -> str:
        try:
            return request.path.split('?')[0].split('/')[-1]
        except IndexError:
            return ''
