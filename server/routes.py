from http.server import BaseHTTPRequestHandler as HTTPRequest
from typing import TypeAlias, Callable

from entities.movies.controllers import MoviesController
from entities.static.controllers import StaticController

from common.http import HttpMethodsType
from paths import Paths


RoutesType: TypeAlias = dict[HttpMethodsType, dict[str, Callable[[HTTPRequest], None]]]


routes: RoutesType  = {
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



__all__ = ('routes',)
