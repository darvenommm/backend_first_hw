"""Module with the helper class for work with http_server request."""
import json
from http.server import BaseHTTPRequestHandler as HTTPRequest
from typing import Any
from urllib.parse import parse_qsl


class Request:
    """Helper class for work with http_server request."""

    @staticmethod
    def parse_queries(request: HTTPRequest) -> dict[str, Any]:
        """Parse get queries from http_server request.

        Args:
            request: request object from http_server.

        Returns:
            dict[str, Any]: parsed get queries.
        """
        if '?' not in request.path:
            return {}

        query_string = request.path.split('?')[1]
        query_couples = (couple.split('=') for couple in query_string.split('&'))

        return {query_key: query_value for (query_key, query_value) in query_couples}

    @staticmethod
    def get_last_segment(request: HTTPRequest) -> str:
        """Get the last url segment from http_sever request.

        Args:
            request: request object from http_server.

        Returns:
            str: the last url segment.
        """
        try:
            return request.path.split('?')[0].split('/')[-1]
        except IndexError:
            return ''

    @staticmethod
    def parse_urlencoded(request: HTTPRequest) -> dict[str, str]:
        """Parse urlencoded data from http_server request.

        Args:
            request: request object from http_server.

        Returns:
            dict[str, str]: parsed data.
        """
        content_length = int(request.headers.get('Content-Length', 0))
        post_data = request.rfile.read(content_length).decode()

        return {field_name: field_value for (field_name, field_value) in parse_qsl(post_data)}

    @staticmethod
    def parse_json(request: HTTPRequest) -> dict[str, str]:
        """Parse json data from http_server request.

        Args:
            request: request object from http_server.

        Returns:
            dict[str, str]: parsed json.
        """
        content_length = int(request.headers.get('Content-Length', 0))
        json_string = request.rfile.read(content_length)

        return json.loads(json_string)
