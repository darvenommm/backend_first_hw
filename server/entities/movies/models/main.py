from typing import Any

from common.regex import regex
from db import DB
from entities.movies.types import MyMovieType
from sqlalchemy import CheckConstraint, UniqueConstraint, delete, select
from sqlalchemy.orm import MappedColumn
from utils.db import UUIDIdMixin


class Movies(UUIDIdMixin, DB):
    __tablename__ = 'movies'

    title: MappedColumn[str]
    imdbID: MappedColumn[str]
    poster: MappedColumn[str]
    plot: MappedColumn[str]
    year: MappedColumn[str]

    @classmethod
    def get_movies(cls):
        with DB.get_session() as session:
            return session.scalars(select(cls)).all()

    @classmethod
    def add(cls, params: MyMovieType) -> None:
        with DB.get_session() as session:
            session.add(cls(**params))
            session.commit()

    @classmethod
    def delete(cls, imdbID: str) -> None:
        with DB.get_session() as session:
            session.execute(delete(cls).where(cls.imdbID == imdbID))
            session.commit()

    __table_args__ = (
        CheckConstraint(
            f"\"imdbID\" ~ '^{regex.IMDB}$'",
            name='check_movies_imdbID_regex',
        ),
        CheckConstraint(
            rf"year ~ '{regex.YEAR}'",
            name='check_movies_year_regex',
        ),

        UniqueConstraint('title', name='unique_movies_title'),
        UniqueConstraint('imdbID', name='unique_movies_imdbID'),
    )
