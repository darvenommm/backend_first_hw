from http.server import BaseHTTPRequestHandler as HTTPRequest

from helpers.template import render_template
from helpers.request import Request
from helpers.response import Response
from api.movies import get_movies


class MoviesApiController:
    @staticmethod
    def get_all(request: HTTPRequest):
        search_title = Request.parse_queries(request).get('search_title')

        if search_title:
            movies_result = get_movies(search_title)
            params = {
                'title': 'Movies API' if movies_result[0] else 'Movies API error',
                'correct_search_title': movies_result[0],
                'movies': movies_result[1] if movies_result[0] else None,
                'error_message': None if movies_result[0] else movies_result[1],
            }
            Response.load_page(request, 200, render_template('movies_api/result', **params))
        else:
            Response.load_page(request, 200, render_template('movies_api/form'))


__all__ = ('MoviesApiController',)
