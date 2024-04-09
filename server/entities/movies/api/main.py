from typing import Any, Literal, NoReturn, TypeAlias, cast

import requests
from entities.movies.types import ApiMovieType, ApiSearchedMovieType
from utils.env_variable import env


class MoviesRequestTypes:
    search: Literal['search'] = 'search'
    title: Literal['get_by_title'] = 'get_by_title'
    imdb: Literal['get_by_imdb'] = 'get_by_imdb'

MoviesRequestType: TypeAlias = (
    Literal['search']
    | Literal['get_by_title']
    | Literal['get_by_imdb']
)


class MoviesApi:
    MOVIES_API_URL = 'http://www.omdbapi.com/'
    MOVIES_API_KEY = env.MOVIES_API_KEY

    @classmethod
    def __get_movies(cls, value: str, request_type: MoviesRequestType, **kwargs) \
            -> list[dict] | dict[str, Any] | NoReturn:
        match request_type:
            case MoviesRequestTypes.search:
                request_type_in_settings = 's'
            case MoviesRequestTypes.title:
                request_type_in_settings = 't'
            case MoviesRequestTypes.imdb | _:
                request_type_in_settings = 'i'

        request_settings = {
            'apikey': cls.MOVIES_API_KEY,
            'type': 'movie',
            'plot': 'full',
            'r': 'json',
            request_type_in_settings: value,
            **kwargs,
        }

        request_result = cast(dict, requests.get(cls.MOVIES_API_URL, request_settings).json())
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
        result: dict[str, Any] = {}

        for (key, value) in movie.items():
            result[key[0].lower() + key[1:] if len(key) > 0 else key] = value

        return result

    @classmethod
    def search_movies(cls, title: str) -> list[ApiSearchedMovieType] | NoReturn:
        movies = cast(list, cls.__get_movies(title, MoviesRequestTypes.search))
        result: list[ApiSearchedMovieType] = []

        for movie in movies:
            result.append(cast(ApiSearchedMovieType, cls.__transform_api_movie(movie)))

        return result

    @classmethod
    def get_movie_by_title(cls, title: str) -> ApiMovieType | NoReturn:
        movie = cast(dict[str, Any], cls.__get_movies(title, MoviesRequestTypes.title))
        return cast(ApiMovieType, cls.__transform_api_movie(movie))

    @classmethod
    def get_movie_by_imdb(cls, imdb: str) -> ApiMovieType | NoReturn:
        movie = cast(dict[str, Any], cls.__get_movies(imdb, MoviesRequestTypes.imdb))
        return cast(ApiMovieType, cls.__transform_api_movie(movie))
