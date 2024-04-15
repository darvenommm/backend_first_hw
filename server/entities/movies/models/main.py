"""Module with class for description movie table."""
from typing import Optional, Sequence

from common.regex import regex
from db import DB
from entities.movies.types import MyMovieType
from sqlalchemy import CheckConstraint, UniqueConstraint, delete, select, update  # noqa: I001, I005
from sqlalchemy.orm import MappedColumn, mapped_column  # noqa: I005
from utils.db import UUIDIdMixin


class Movies(UUIDIdMixin, DB):
    """Class for description movie table."""

    __tablename__ = 'movies'

    title: MappedColumn[str]
    imdb: MappedColumn[str]
    poster: MappedColumn[str]
    plot: MappedColumn[str]
    year: MappedColumn[str]
    note: MappedColumn[Optional[str]] = mapped_column(default='')

    @classmethod
    def get_movies(cls) -> Sequence:
        """Get all movies from the db.

        Returns:
            Sequence: sequence of movies.
        """
        with DB.get_session() as session:
            return session.scalars(select(cls)).all()

    @classmethod
    def add(cls, fields: MyMovieType) -> None:
        """Add movie to the db.

        Args:
            fields: fields for adding movie.
        """
        with DB.get_session() as session:
            session.add(cls(**fields))
            session.commit()

    @classmethod
    def delete(cls, imdb: str) -> None:
        """Delete movie by imdb.

        Args:
            imdb: imdb of the deleted movie.
        """
        with DB.get_session() as session:
            session.execute(delete(cls).where(cls.imdb == imdb))
            session.commit()

    @classmethod
    def update_note(cls, imdb: str, new_note: str) -> None:
        """Update the movie note.

        Args:
            imdb: imdb of the deleted movie.
            new_note: new note for the movie.
        """
        with DB.get_session() as session:
            query = update(cls).where(cls.imdb == imdb).values(note=new_note)
            session.execute(query)
            session.commit()

    __table_args__ = (
        CheckConstraint(
            f"\"imdb\" ~ '^{regex.IMDB}$'",
            name='check_movies_imdb_regex',
        ),
        CheckConstraint(
            rf"year ~ '{regex.YEAR}'",
            name='check_movies_year_regex',
        ),

        UniqueConstraint('title', name='unique_movies_title'),
        UniqueConstraint('imdb', name='unique_movies_imdb'),
    )
