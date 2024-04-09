import re
from http.server import BaseHTTPRequestHandler
from typing import Callable, TypeAlias

from common.http import HttpMethodsType, http_methods
from entities.movies.controllers import MoviesController
from entities.static.controllers import StaticController
from paths import Paths

RoutesControllerHandler = Callable[[BaseHTTPRequestHandler], None]
RoutesType: TypeAlias = dict[HttpMethodsType, dict[str, RoutesControllerHandler]]


class Router:
    __routes: RoutesType = {
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
        'DELETE': {
            Paths.my_movie: MoviesController.delete,
        },
    }

    @classmethod
    def __find_handler(cls, method: HttpMethodsType) -> Callable:
        def inner(request: BaseHTTPRequestHandler) -> None:
            for (path, controller_handler) in cls.__routes.get(method, {}).items():
                given_path = request.path.split('?')[0].rstrip('/')
                checking_path = rf'^{path.rstrip('/')}$'

                if bool(re.match(checking_path, given_path)):
                    return controller_handler(request)
        return inner

    @classmethod
    def add_routing(cls, http_server: type) -> type:
        for method in http_methods:
            setattr(http_server, f'do_{method}', cls.__find_handler(method))

        return http_server
