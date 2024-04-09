from http.server import BaseHTTPRequestHandler as HTTPRequest

from entities.movies.models import Movies
from entities.movies.api import MoviesApi
from entities.movies.types import MyMovieType
from utils.response import Response
from utils.request import Request
from utils.render import Render
from paths import Paths
from common.http import http_statuses


class MoviesController:
    @staticmethod
    def get_mine(request: HTTPRequest) -> None:
        parameters = {
            'movies': Movies.get_movies(),
            'current_path': Paths.my_movies,
            'title': 'My movie',
        }
        page = Render.render_template('movies/my_movies', **parameters)
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

        parameters = {'movies': movies, 'title': 'Movies', 'current_path': Paths.movies}
        Response.load_page(request, Render.render_template('movies/movies', **parameters))

    @staticmethod
    def get_one(request: HTTPRequest) -> None:
        try:
            movie = MoviesApi.get_movie_by_imdb(Request.get_last_segment(request))
        except ValueError as exception:
            return Response.send_bad_request(request, str(exception))

        parameters = {'movie': movie, 'title': 'Movie'}
        Response.load_page(request, Render.render_template('movies/movie', **parameters))


    @staticmethod
    def get_movie_search_form(request: HTTPRequest) -> None:
        parameters = {'current_path': Paths.home}
        Response.load_page(request, Render.render_template('movies/search_form', **parameters))

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
            'imdbID': movie['imdbID'],
            'plot': movie['plot'],
            'poster': movie['poster'],
            'year': movie['year'],
        }

        Movies.add(new_movie)

        Response.redirect(request, Paths.my_movies, http_statuses.REDIRECT_FOUND)


    @staticmethod
    def delete(request: HTTPRequest) -> None:
        Movies.delete(Request.get_last_segment(request))

        Response.set_response(request, http_statuses.OK)
