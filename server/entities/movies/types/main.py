"""Module with movies types."""
from typing import NotRequired, Required, TypedDict


class MyMovieType(TypedDict):
    """Type for my movie from db."""

    title: Required[str]
    imdb: Required[str]
    poster: Required[str]
    plot: Required[str]
    year: Required[str]
    note: NotRequired[str]


class ApiBaseMovieType(TypedDict):
    """Base movie type from movie api."""

    title: Required[str]
    imdb: Required[str]
    year: Required[str]
    poster: Required[str]
    type: Required[str]


class ApiSearchedMovieType(ApiBaseMovieType):
    """Type for movies search."""


class ApiMovieType(ApiBaseMovieType):
    """Type for full movie information."""

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
