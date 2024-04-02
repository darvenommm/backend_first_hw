from http.server import BaseHTTPRequestHandler as HttpRequest

from utils.render import Render
from common.http_statuses import http_statuses


class Response:
    @staticmethod
    def load_page(
        request: HttpRequest,
        body: str = '',
        status: int = http_statuses.OK,
        headers: list[tuple[str, str]] = list(),
    ) -> None:
        request.send_response(status)
        request.send_header('Content-type', 'text/html')

        for header in headers:
            request.send_header(*header)
        else:
            request.end_headers()

        request.wfile.write(body.encode())

    @staticmethod
    def send_bad_request(
        request: HttpRequest,
        error_message: str = 'Bad User Request',
        status: int = http_statuses.USER_BAD,
        headers: list[tuple[str, str]] = list(),
    ) -> None:
        request.send_response(status)
        request.send_header('Content-type', 'text/html')

        for header in headers:
            request.send_header(*header)
        else:
            request.end_headers()

        request.wfile.write(
            Render.render_template('pages/error', error_message=error_message).encode()
        )

