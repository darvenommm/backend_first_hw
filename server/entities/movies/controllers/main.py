from http.server import BaseHTTPRequestHandler as HTTPRequest

from common.http import http_statuses
from entities.movies.api import MoviesApi
from entities.movies.models import Movies
from entities.movies.types import MyMovieType
from paths import Paths
from sqlalchemy.exc import SQLAlchemyError
from utils.render import Render
from utils.request import Request
from utils.response import Response


class MoviesController:
    @staticmethod
    def load_mine(request: HTTPRequest) -> None:
        page_parameters = {
            'movies': Movies.get_movies(),
            'current_path': Paths.my_movies,
            'title': 'My movie',
        }
        page = Render.render_template('movies/my_movies', **page_parameters)
        Response.load_page(request, page)

    @staticmethod
    def load_all(request: HTTPRequest) -> None:
        search_title = Request.parse_queries(request).get('search_title')

        if not search_title:
            return Response.send_bad_request(request)

        try:
            movies = MoviesApi.search_movies(search_title)
        except ValueError as exception:
            return Response.send_bad_request(request, str(exception))

        page_parameters = {'movies': movies, 'title': 'Movies', 'current_path': Paths.movies}
        Response.load_page(request, Render.render_template('movies/movies', **page_parameters))

    @staticmethod
    def load_one(request: HTTPRequest) -> None:
        try:
            movie = MoviesApi.get_movie_by_imdb(Request.get_last_segment(request))
        except ValueError as exception:
            return Response.send_bad_request(request, str(exception))

        page_parameters = {'movie': movie, 'title': 'Movie'}
        Response.load_page(request, Render.render_template('movies/movie', **page_parameters))

    @staticmethod
    def load_search_form(request: HTTPRequest) -> None:
        page_parameters = {'current_path': Paths.home}

        Response.load_page(
            request,
            Render.render_template('movies/search_form', **page_parameters),
        )

    @staticmethod
    def add(request: HTTPRequest) -> None:
        imdb = Request.parse_urlencoded(request).get('imdb')

        if not imdb:
            return Response.send_bad_request(request)

        try:
            movie = MoviesApi.get_movie_by_imdb(imdb)
        except ValueError as exception:
            return Response.send_bad_request(request, str(exception))

        new_movie: MyMovieType = {
            'title': movie['title'],
            'imdb': movie['imdb'],
            'plot': movie['plot'],
            'poster': movie['poster'],
            'year': movie['year'],
        }

        try:
            Movies.add(new_movie)
        except SQLAlchemyError:
            return Response.send_bad_request(request)

        Response.redirect(request, Paths.my_movies, http_statuses.CREATED)

    @staticmethod
    def delete(request: HTTPRequest) -> None:
        Movies.delete(Request.get_last_segment(request))

        Response.set_response(request, http_statuses.NO_CONTENT)

    @staticmethod
    def update(request: HTTPRequest) -> None:
        imdb = Request.get_last_segment(request)

        try:
            note = Request.parse_json(request)['note']
        except KeyError:
            return Response.send_bad_request(request)

        Movies.update_note(imdb, note)

        Response.set_response(request, http_statuses.NO_CONTENT)
