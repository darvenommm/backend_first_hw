"""Module with the helper class for work with http_server responses."""
from http.server import BaseHTTPRequestHandler as HttpRequest

from common.http import http_statuses
from utils.render import Render


class Response:
    """Helper class for work with http_server responses."""

    @staticmethod
    def set_response(
        request: HttpRequest,
        status: int,
        headers: list[tuple[str, str]] | None = None,
        body: str = '',
        content_type: str | None = 'text/html',
    ) -> None:
        """Create a custom responses with the given parameters.

        Args:
            request: request object from http_server.
            status: response status.
            headers: list of response headers. Defaults to None.
            body: response text body. Defaults to ''.
            content_type: Content-Type for the response. Defaults to 'text/html'.
        """
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
        """Load a html page for user.

        Args:
            request: request object from http_server.
            body: response text body. Defaults to ''.
            status: response status. Defaults to http_statuses.OK.
            headers: list of response headers. Defaults to None.
        """
        cls.set_response(request, status, headers, body)

    @classmethod
    def send_bad_request(
        cls,
        request: HttpRequest,
        error_message: str = 'Bad User Request',
        status: int = http_statuses.USER_BAD,
        headers: list[tuple[str, str]] | None = None,
    ) -> None:
        """Load a html page with a bad request message.

        Args:
            request: request object from http_server.
            error_message: error message for the user. Defaults to 'Bad User Request'.
            status: response status. Defaults to http_statuses.USER_BAD.
            headers: list of response headers. Defaults to None.
        """
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
        """Redirect the user to a other page.

        Args:
            request: request object from http_server.
            url: url for redirecting.
            status: response status. Defaults to http_statuses.REDIRECT_FOUND.
            headers: list of response headers. Defaults to None.
        """
        headers = [] if headers is None else headers

        if status // 100 == 3:
            headers.append(('Location', url))
        else:
            headers.append(('Refresh', f'0; {url=}'))

        cls.set_response(request, status, headers, content_type=None)
