"""Module with paths."""
from common.regex import regex


class Paths:
    """Class with paths."""

    home = '/'
    movie = f'/movies/{regex.IMDB}'
    movies = '/movies'

    my_movie = f'/my-movies/{regex.IMDB}'
    my_movies = '/my-movies'

    styles = '/styles.css'
    movies_js = '/movies.js'
