from http.server import BaseHTTPRequestHandler as HTTPRequest

from entities.movies.models import Movies
from entities.movies.api import MoviesApi
from entities.movies.types import MyMovieType
from utils.response import Response
from utils.request import Request
from utils.render import Render
from paths import Paths
from common.http_statuses import http_statuses


class MoviesController:
    @staticmethod
    def get_mine(request: HTTPRequest) -> None:
        page = Render.render_template('movies/my_movies', movies=Movies.get_movies())
        Response.load_page(request, page)

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
        imdb = Request.parse_urlencoded(request).get('imdbID')

        if not imdb:
            return Response.send_bad_request(request)

        try:
            movie = MoviesApi.get_movie_by_imdb(imdb)
        except ValueError as exception:
            return Response.send_bad_request(request, str(exception))

        new_movie: MyMovieType = {
            'title': movie['title'],
            'imdb': movie['imdbID'],
            'plot': movie['plot'],
            'poster': movie['poster'],
        }

        Movies.add(new_movie)

        Response.redirect(request, Paths.my_movies, http_statuses.REDIRECT_FOUND)


    @staticmethod
    def delete(request: HTTPRequest) -> None:
        pass
