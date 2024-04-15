"""Module with MoviesApi class."""
from typing import Any, Literal, NoReturn, TypeAlias, cast

import requests
from entities.movies.types import ApiMovieType, ApiSearchedMovieType
from utils.env_variable import env


class MoviesRequestTypes:
    """Type of movies request variants."""

    search: Literal['search'] = 'search'
    title: Literal['get_by_title'] = 'get_by_title'
    imdb: Literal['get_by_imdb'] = 'get_by_imdb'


MoviesRequestType: TypeAlias = (
    Literal['search']
    | Literal['get_by_title']
    | Literal['get_by_imdb']
)


class MoviesApi:
    """Class for working with movies api."""

    movies_api_url = 'http://www.omdbapi.com/'
    movies_api_key = env.MOVIES_API_KEY

    @classmethod
    def search_movies(cls, title: str) -> list[ApiSearchedMovieType] | NoReturn:
        """Search movies by title.

        Args:
            title: movies title.

        Returns:
            list[ApiSearchedMovieType] | NoReturn: list movies or ValueError
        """
        movies = cast(list, cls.__get_movies(title, MoviesRequestTypes.search))
        movies_result: list[ApiSearchedMovieType] = []

        for movie in movies:
            movies_result.append(cast(ApiSearchedMovieType, cls.__transform_api_movie(movie)))

        return movies_result

    @classmethod
    def get_movie_by_title(cls, title: str) -> ApiMovieType | NoReturn:
        """Get movie by title.

        Args:
            title: movie title.

        Returns:
            ApiMovieType | NoReturn: movie or ValueError
        """
        movie = cast(dict[str, Any], cls.__get_movies(title, MoviesRequestTypes.title))
        return cast(ApiMovieType, cls.__transform_api_movie(movie))

    @classmethod
    def get_movie_by_imdb(cls, imdb: str) -> ApiMovieType | NoReturn:
        """Get movie by imdb.

        Args:
            imdb: movie imdb.

        Returns:
            ApiMovieType | NoReturn: Movie or ValueError
        """
        movie = cast(dict[str, Any], cls.__get_movies(imdb, MoviesRequestTypes.imdb))
        return cast(ApiMovieType, cls.__transform_api_movie(movie))

    @classmethod
    def __get_movies(
        cls,
        identifier: str,
        request_type: MoviesRequestType,
        **kwargs,
    ) -> list[dict] | dict[str, Any] | NoReturn:
        """Get movies by some identifier.

        Args:
            identifier: value of movies searching.
            request_type: type of movies searching.
            kwargs: extra parameters for request to movies api.

        Raises:
            ValueError: If request returned with some exception.

        Returns:
            list[dict] | dict[str, Any] | NoReturn: movies list or movies or ValueError.
        """
        match request_type:
            case MoviesRequestTypes.search:
                request_type_in_settings = 's'
            case MoviesRequestTypes.title:
                request_type_in_settings = 't'
            case MoviesRequestTypes.imdb | _:
                request_type_in_settings = 'i'

        request_settings = {
            'apikey': cls.movies_api_key,
            'type': 'movie',
            'plot': 'full',
            'r': 'json',
            request_type_in_settings: identifier,
            **kwargs,
        }

        request_result = cast(
            dict,
            requests.get(
                cls.movies_api_url,
                request_settings,
                timeout=10,
            ).json(),
        )
        request_status = request_result.get('Response', 'False')

        if request_status == 'False':
            raise ValueError(request_result.get('Error', ''))

        match request_type:
            case MoviesRequestTypes.search:
                return cast(list, request_result.get('Search', []))
            case MoviesRequestTypes.title | MoviesRequestTypes.imdb | _:
                return request_result

    @staticmethod
    def __transform_api_movie(movie: dict[str, Any]) -> dict[str, Any]:
        result_movie: dict[str, Any] = {}

        for (movie_key, movie_value) in movie.items():
            movie_key = movie_key[0].lower() + movie_key[1:]
            movie_key = 'imdb' if movie_key == 'imdbID' else movie_key
            result_movie[movie_key] = movie_value

        return result_movie
