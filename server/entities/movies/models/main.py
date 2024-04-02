from typing import Any
from sqlalchemy import CheckConstraint, UniqueConstraint, select
from sqlalchemy.orm import MappedColumn

from db import DB

from common.regex import regex
from utils.db import UUIDIdMixin


class Movies(UUIDIdMixin, DB):
    __tablename__ = 'movies'

    title: MappedColumn[str]
    imdb: MappedColumn[str]
    poster: MappedColumn[str]
    plot: MappedColumn[str]

    __table_args__ = (
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
