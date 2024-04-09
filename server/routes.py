from http.server import BaseHTTPRequestHandler
import re
from typing import cast, TypeAlias, Callable

from entities.movies.controllers import MoviesController
from entities.static.controllers import StaticController

from common.http import HttpMethodsType
from paths import Paths


RoutesType: TypeAlias = dict[HttpMethodsType, dict[str, Callable[[BaseHTTPRequestHandler], None]]]


class Routes:
    __routes: RoutesType  = {
        'GET': {
            Paths.home: MoviesController.get_movie_search_form,
            Paths.movies: MoviesController.get_all,
            Paths.movie: MoviesController.get_one,
            Paths.my_movies: MoviesController.get_mine,

            Paths.styles: StaticController.get_styles,
        },
        'POST': {
            Paths.my_movies: MoviesController.add,
        },
        'PUT': {},
        'PATCH': {},
        'DELETE': {
            Paths.my_movie: MoviesController.delete,
        },
        'HEAD': {},
    }

    @classmethod
    def __find_handler(cls, method: HttpMethodsType) -> Callable:
        def inner(request: BaseHTTPRequestHandler) -> None:
            for (path, handler) in cls.__routes.get(method, {}).items():
                given_path = request.path.split('?')[0].rstrip('/')
                if bool(re.match(rf'^{path.rstrip('/')}$', given_path)):
                    return handler(request)
        return inner

    @classmethod
    def __add_routes(cls, http_server: type) -> type:
        methods = cast(tuple[HttpMethodsType, ...], getattr(http_server, 'methods', tuple))

        for method in methods:
            setattr(http_server, f'do_{method}', cls.__find_handler(method))

        return http_server

    def __init__(self, http_server: type) -> None:
        self.__http_server = http_server

    def __call__(self, *args, **kwargs) -> type:
        return self.__add_routes(self.__http_server)(*args, **kwargs)


__all__ = ('Routes',)
