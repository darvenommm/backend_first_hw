from http.server import BaseHTTPRequestHandler


class Response:
    @staticmethod
    def load_page(
        request: 'BaseHTTPRequestHandler',
        status: int,
        body: str = '',
        headers: list[tuple[str, str]] = list(),
        encoding: str = 'utf-8',
    ) -> None:
        request.send_response(status)

        request.send_header('Content-type', 'text/html')

        for header in headers:
            request.send_header(*header)
        else:
            request.end_headers()

        request.wfile.write(body.encode(encoding))
