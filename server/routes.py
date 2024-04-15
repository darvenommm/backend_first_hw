"""Module with paths router."""
import re
from http.server import BaseHTTPRequestHandler
from typing import Callable, TypeAlias

from common.http import HttpMethodsType, http_methods
from entities.movies.controllers import MoviesController
from paths import Paths
from utils.static import StaticHandler

RoutesControllerHandler = Callable[[BaseHTTPRequestHandler], None]
RoutesType: TypeAlias = dict[HttpMethodsType, dict[str, RoutesControllerHandler]]


routes: RoutesType = {
    'GET': {
        Paths.home: MoviesController.load_search_form,
        Paths.movies: MoviesController.load_all,
        Paths.movie: MoviesController.load_one,
        Paths.my_movies: MoviesController.load_mine,
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
    """Class for adding routes to http_server."""

    @classmethod
    def add_routing(cls, http_server: type) -> type:
        """Add routing for http_server.

        Args:
            http_server: python http server.

        Returns:
            type: modified http server.
        """
        for method in http_methods:
            setattr(http_server, f'do_{method}', cls.__create_method_handler(method))

        return http_server

    @staticmethod
    def __create_method_handler(method: HttpMethodsType) -> Callable:
        """Create handler for http methods.

        Args:
            method: http methods.

        Returns:
            Callable: http method handler.
        """
        def inner(request: BaseHTTPRequestHandler) -> None:
            given_path = request.path.split('?')[0].rstrip('/')

            for (path, controller_handler) in routes.get(method, {}).items():
                path = path.rstrip('/')
                checking_path = rf'^{path}$'

                if bool(re.match(checking_path, given_path)):
                    return controller_handler(request)

            if method == 'GET':
                StaticHandler.handle_path(request, given_path)

        return inner
