from typing import Any
from sqlalchemy import CheckConstraint, UniqueConstraint, select
from sqlalchemy.orm import MappedColumn

from db import DB

from common.regex import regex
from utils.db import UUIDIdMixin
from entities.movies.types import MyMovieType


class Movies(UUIDIdMixin, DB):
    __tablename__ = 'movies'

    title: MappedColumn[str]
    imdb: MappedColumn[str]
    poster: MappedColumn[str]
    plot: MappedColumn[str]

    @classmethod
    def get_movies(cls):
        with DB.get_session() as session:
            return session.scalars(select(cls)).all()

    @classmethod
    def add(cls, params: MyMovieType) -> None:
        with DB.get_session() as session:
            session.add(cls(**params))
            session.commit()

    __table_args__ = (
        CheckConstraint(
            f"imdb ~ '^{regex.IMDB}$'",
            name='check_movies_imdb_regex',
        ),

        UniqueConstraint('title', name='unique_movies_title'),
        UniqueConstraint('imdb', name='unique_movies_imdb'),
    )
