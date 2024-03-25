from typing import cast, TypedDict, Required, TypeAlias

import requests

import config


class MovieBaseType(TypedDict):
    title: Required[str]
    year: Required[str]
    imdbID: Required[str]
    poster: Required[str]


class MovieSearchType(MovieBaseType):
    pass

class MovieType(MovieBaseType):
    rated: Required[str]
    released: Required[str]
    runtime: Required[str]
    genre: Required[list[str]]
    director: Required[list[str]]
    writer: Required[list[str]]
    actors: Required[list[str]]
    plot: Required[str]
    language: Required[list[str]]
    awards: Required[str]
    country: Required[list[str]]
    metascore: Required[str]

MessageErrorType: TypeAlias = str


class MovieApi:
    @staticmethod
    def __send_request(
        identifier: str,
        is_search: bool = True,
        use_title: bool = True,
        params: dict[str, str] = dict()
    ):
        request_key = 's' if is_search else ('t' if use_title else 'i')

        return requests.get(config.MOVIES_API_URL, {
            'apikey': config.MOVIES_API_KEY,
            'type': 'movie',
            'plot': 'full',
            'r': 'json',
            request_key: identifier,
            **params,
        })

    @staticmethod
    def transform_to_correct_form(parameters: dict[str, str]) -> dict[str, str | list[str]]:
        result: dict[str, str | list[str]] = {}
        list_parameters = ('genre', 'director', 'writer', 'actors', 'language', 'country')

        for (key, value) in parameters.items():
            key = key[0].lower() + key[1:]
            result[key] = value if key not in list_parameters else value.split(', ')

        return result

    @classmethod
    def search_movies(cls, identifier: str, use_title: bool = True) \
            -> tuple[bool, list[MovieSearchType] | MessageErrorType]:
        result = cast(
            dict,
            cls.__send_request(identifier, is_search=True, use_title=use_title).json()
        )
        status = not (result.get('Response') == 'False')

        if status:
            movies: list[dict[str, str | list[str]]] = []

            for movie in result.get('Search', list()):
                movie = cast(dict[str, str], movie)
                movies.append(cls.transform_to_correct_form(movie))

            result_movies: list[MovieSearchType] = movies # type: ignore

        return (status, result_movies if status else result.get('Error', ''))

    @classmethod
    def get_movie(cls, identifier: str, use_title: bool = True) \
            -> tuple[bool, MovieType | MessageErrorType]:
        result = cast(
            dict[str, str],
            cls.__send_request(identifier, is_search=False, use_title=use_title).json()
        )
        status = not (result.get('Response') == 'False')

        if status:
            movie: dict[str, str | list[str]] = cls.transform_to_correct_form(result)
            result_movie: MovieType = movie # type: ignore

        return (status, result_movie if status else result.get('Error', ''))


__all__ = ('MovieType', 'MovieSearchType', 'MovieApi')
