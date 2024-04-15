"""Module with class that handles static files."""
from functools import lru_cache
from http.server import BaseHTTPRequestHandler as HTTPRequest
from os.path import exists, isfile

from common.http import http_statuses
from utils.path import PathsHelper
from utils.response import Response


class StaticHandler:
    """Class for handing static files."""

    __static_directory = PathsHelper.create_absolute_path('static').as_posix()

    @classmethod
    def handle_path(cls, request: HTTPRequest, path: str) -> None:
        """Handle static by its path.

        Args:
            request: request object from http_server.
            path: static path.
        """
        file_path = f'{cls.__static_directory}{path}'

        if (not exists(file_path)) or (not isfile(file_path)):
            return

        file_text = cls.__get_file_text(file_path)

        Response.set_response(request, http_statuses.OK, body=file_text, content_type=None)

    @staticmethod
    @lru_cache
    def __get_file_text(path: str) -> bytes:
        """Get file text with caching.

        Args:
            path: file path.

        Returns:
            bytes: file text in bytes.
        """
        with open(path, 'rb') as text_file:
            return text_file.read()
