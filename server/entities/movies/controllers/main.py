from http.server import BaseHTTPRequestHandler as HTTPRequest

from entities.movies.api import MoviesApi
from utils.response import Response
from utils.request import Request
from utils.render import Render


class MoviesController:
    @staticmethod
    def get_mine(request: HTTPRequest) -> None:
        pass

    @staticmethod
    def get_all(request: HTTPRequest) -> None:
        search_title = Request.parse_queries(request).get('search_title')

        if not search_title:
            return Response.send_bad_request(request)

        try:
            movies = MoviesApi.search_movies(search_title)
        except ValueError as exception:
            return Response.send_bad_request(request, str(exception))

        Response.load_page(request, Render.render_template('movies/movies', movies=movies))

    @staticmethod
    def get_one(request: HTTPRequest) -> None:
        try:
            movie = MoviesApi.get_movie_by_imdb(Request.get_last_segment(request))
        except ValueError as exception:
            return Response.send_bad_request(request, str(exception))

        Response.load_page(request, Render.render_template('movies/movie', movie=movie))


    @staticmethod
    def get_movie_search_form(request: HTTPRequest) -> None:
        Response.load_page(request, Render.render_template('movies/search_form'))

    @staticmethod
    def add(request: HTTPRequest) -> None:
        pass

    @staticmethod
    def delete(request: HTTPRequest) -> None:
        pass
