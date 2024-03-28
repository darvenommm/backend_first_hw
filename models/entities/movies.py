from typing import Any
from sqlalchemy import CheckConstraint, UniqueConstraint, select
from sqlalchemy.orm import MappedColumn, Mapped, relationship

from models.base import Base, get_session
from models.entities import movies_actors

from constants import regex
from helpers.models import UUIDIdMixin


class Movies(UUIDIdMixin, Base):
    __tablename__ = 'movies'

    @classmethod
    def get_movies(cls):
        with get_session() as session:
            return session.scalar(select(cls))

    @classmethod
    def add(cls, title: str, year: int, imdb: str, poster: str) -> None:
        with get_session() as session:
            new_movie = cls(title=title, year=year, imdb=imdb, poster=poster)
            session.add(new_movie)

    @property
    def actors(self):
        return self.movies_actors.actors

    title: MappedColumn[str]
    year: MappedColumn[int]
    imdb: MappedColumn[str]
    poster: MappedColumn[str]

    movies_actors: Mapped['movies_actors.MoviesActors'] = relationship(
        back_populates='movies',
        cascade='all, delete-orphan',
    )

    __table_args__ = (
        CheckConstraint(
            'length(title) < 50',
            name='check_movies_title_length',
        ),
        CheckConstraint(
            f"imdb ~ '^{regex.IMDB}$'",
            name='check_movies_imdb_regex',
        ),
        CheckConstraint(
            f"poster = 'N/A' OR poster ~ '{regex.URL}'",
            name='check_movies_imdb_poster',
        ),

        UniqueConstraint('title', name='unique_movies_title'),
        UniqueConstraint('imdb', name='unique_movies_imdb'),
    )

__all__ = ('Movies',)
