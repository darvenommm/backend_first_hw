from http.server import BaseHTTPRequestHandler as HTTPRequest
from typing import Any
from urllib.parse import parse_qsl


class Request:
    @staticmethod
    def parse_queries(request: HTTPRequest) -> dict[str, Any]:
        if '?' not in request.path:
            return {}

        query_string = request.path.split('?')[1]
        query_couples = (couple.split('=') for couple in query_string.split('&'))

        return {query_key: query_value for (query_key, query_value) in query_couples}

    @staticmethod
    def get_last_segment(request: HTTPRequest) -> str:
        try:
            return request.path.split('?')[0].split('/')[-1]
        except IndexError:
            return ''

    @staticmethod
    def parse_urlencoded(request: HTTPRequest) -> dict[str, str]:
        content_length = int(request.headers.get('Content-Length', 0))
        post_data = request.rfile.read(content_length).decode()

        return {field_name: field_value for (field_name, field_value) in parse_qsl(post_data)}
