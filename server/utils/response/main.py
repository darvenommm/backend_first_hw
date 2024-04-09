from http.server import BaseHTTPRequestHandler as HttpRequest

from common.http import http_statuses
from utils.render import Render


class Response:
    @staticmethod
    def set_response(
        request: HttpRequest,
        status: int,
        headers: list[tuple[str, str]] | None = None,
        body: str = '',
        content_type: str | None = 'text/html',
    ) -> None:
        request.send_response(status)

        if content_type:
            request.send_header('Content-type', content_type)

        if headers:
            for header in headers:
                request.send_header(*header)

        request.end_headers()

        if body:
            request.wfile.write(body.encode())

    @classmethod
    def load_page(
        cls,
        request: HttpRequest,
        body: str = '',
        status: int = http_statuses.OK,
        headers: list[tuple[str, str]] | None = None,
    ) -> None:
        cls.set_response(request, status, headers, body)

    @classmethod
    def send_bad_request(
        cls,
        request: HttpRequest,
        error_message: str = 'Bad User Request',
        status: int = http_statuses.USER_BAD,
        headers: list[tuple[str, str]] | None = None,
    ) -> None:
        page = Render.render_template('pages/error', error_message=error_message, title='Error')
        cls.set_response(request, status, headers, page)

    @classmethod
    def redirect(
        cls,
        request: HttpRequest,
        url: str,
        status: int = http_statuses.REDIRECT_FOUND,
        headers: list[tuple[str, str]] | None = None,
    ) -> None:
        headers = [('Location', url)]

        cls.set_response(request, status, headers, content_type=None)
