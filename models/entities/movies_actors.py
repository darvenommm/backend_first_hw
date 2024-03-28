from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import MappedColumn, mapped_column, Mapped, relationship

from models.base import Base

from helpers.models import UUIDIdMixin
from models.entities import movies, actors


class MoviesActors(UUIDIdMixin, Base):
    __tablename__ = 'movies_actors'

    movie_id: MappedColumn[UUID] = mapped_column(ForeignKey('movies.id'))
    actor_id: MappedColumn[UUID] = mapped_column(ForeignKey('actors.id'))

    actors: Mapped['actors.Actors'] = relationship(back_populates='movies_actors')
    movies: Mapped['movies.Movies'] = relationship(back_populates='movies_actors')

    __table_args__ = (
        UniqueConstraint(
            'movie_id',
            'actor_id', name='unique_movies_actors_movie_id_and_actor_id',
        ),
    )


__all__ = ('MoviesActors',)
