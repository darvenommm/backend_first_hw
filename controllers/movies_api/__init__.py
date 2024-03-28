from http.server import BaseHTTPRequestHandler as HTTPRequest

from helpers.template import render_template
from helpers.request import Request
from helpers.response import Response
from api.movies import MovieApi
from constants import request_status


class MoviesApiController:
    @staticmethod
    def get_all(request: HTTPRequest) -> None:
        search_title = Request.parse_queries(request).get('search_title')

        if not search_title:
            Response.load_page(request, request_status.OK, render_template('movies_api/form'))
            return

        (is_ok, result) = MovieApi.search_movies(search_title, use_title=True)

        if not is_ok:
            Response.load_page(request, request_status.USER_BAD, render_template(
                'error',
                error_message=result,
                title='Movies API error'
            ))
        else:
            Response.load_page(request, request_status.OK, render_template(
                'movies_api/movies',
                title='Movies API',
                movies=result
            ))

    @staticmethod
    def get_one(request: HTTPRequest) -> None:
        (is_ok, result) = MovieApi.get_movie(Request.get_last_segment(request), use_title=False)

        if not is_ok:
            return Response.load_page(request, request_status.USER_BAD, render_template(
                'error',
                error_message=result,
                title='Movies API error'
            ))

        Response.load_page(request, request_status.OK, render_template(
            'movies_api/movie',
            movie=result,
        ))


__all__ = ('MoviesApiController',)
