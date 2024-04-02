from typing import TypedDict, Required


class MyMovieType(TypedDict):
    title: Required[str]
    imdb: Required[str]
    poster: Required[str]
    plot: Required[str]


class ApiBaseMovieType(TypedDict):
    title: Required[str]
    imdbID: Required[str]
    year: Required[str]
    poster: Required[str]
    type: Required[str]


class ApiSearchedMovieType(ApiBaseMovieType):
    pass


class ApiMovieType(ApiBaseMovieType):
    rated: Required[str]
    released: Required[str]
    runtime: Required[str]
    genre: Required[str]
    director: Required[str]
    writer: Required[str]
    actors: Required[str]
    plot: Required[str]
    language: Required[str]
    awards: Required[str]
    country: Required[str]
    metascore: Required[str]
