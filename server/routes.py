import re
from http.server import BaseHTTPRequestHandler
from typing import Callable, TypeAlias

from common.http import HttpMethodsType, http_methods
from entities.movies.controllers import MoviesController
from entities.static.controllers import StaticController
from paths import Paths

RoutesControllerHandler = Callable[[BaseHTTPRequestHandler], None]
RoutesType: TypeAlias = dict[HttpMethodsType, dict[str, RoutesControllerHandler]]


routes: RoutesType = {
    'GET': {
        Paths.home: MoviesController.load_search_form,
        Paths.movies: MoviesController.load_all,
        Paths.movie: MoviesController.load_one,
        Paths.my_movies: MoviesController.load_mine,

        Paths.styles: StaticController.load_styles,
        Paths.movies_js: StaticController.load_movies_js,
    },
    'POST': {
        Paths.my_movies: MoviesController.add,
    },
    'DELETE': {
        Paths.my_movie: MoviesController.delete,
    },
    'PATCH': {
        Paths.my_movie: MoviesController.update,
    },
}


class Router:
    @classmethod
    def add_routing(cls, http_server: type) -> type:
        for method in http_methods:
            setattr(http_server, f'do_{method}', cls.__create_method_handler(method))

        return http_server

    @staticmethod
    def __create_method_handler(method: HttpMethodsType) -> Callable:
        def inner(request: BaseHTTPRequestHandler) -> None:
            for (path, controller_handler) in routes.get(method, {}).items():
                path = path.rstrip('/')
                given_path = request.path.split('?')[0].rstrip('/')

                checking_path = rf'^{path}$'

                if bool(re.match(checking_path, given_path)):
                    return controller_handler(request)
        return inner
