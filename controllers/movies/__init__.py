from http.server import BaseHTTPRequestHandler as HTTPRequest


class MoviesController:
    @staticmethod
    def get_all(request: HTTPRequest):
        pass

    @staticmethod
    def create(request: HTTPRequest):
        print(request, 'hello')
        pass

    @staticmethod
    def change(request: HTTPRequest):
        pass

    @staticmethod
    def delete(request: HTTPRequest):
        pass


__all__ = ('MoviesController',)
