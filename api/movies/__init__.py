from typing import TypedDict, Required, Literal

import requests # type: ignore

import config


class MovieType(TypedDict):
    Title: Required[str]
    Year: Required[str]
    imdbID: Required[str]
    Type: Required[Literal['movie']]
    Poster: Required[str] # url or N/A


# returning tuple: 1 -> result of request (False=Error, True=OK), 2 -> list of movies or error message
def get_movies(name_part: str) -> tuple[bool, list[MovieType] | str]:
    result: dict = requests.get(config.MOVIES_API_URL, {
        'apikey': config.MOVIES_API_KEY,
        'type': 'movie',
        'plot': 'full',
        'r': 'json',
        's': name_part,
    }).json()

    status = (result.get('Response') != 'False')

    return (status, result['Search'] if status else result['Error'])


__all__ = ('get_movies',)
