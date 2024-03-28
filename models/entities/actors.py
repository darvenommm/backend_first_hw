from sqlalchemy import CheckConstraint
from sqlalchemy.orm import MappedColumn, Mapped, relationship

from models.base import Base
from models.entities import movies_actors

from helpers.models import UUIDIdMixin


class Actors(UUIDIdMixin, Base):
    __tablename__ = 'actors'

    @property
    def movies(self):
        return self.movies_actors.movies

    name: MappedColumn[str]
    surname: MappedColumn[str]

    movies_actors: Mapped['movies_actors.MoviesActors'] = relationship(
        back_populates='actors',
        cascade='all, delete-orphan',
    )

    __table_args__ = (
        CheckConstraint('length(name) < 40', name='check_actors_name_length'),
        CheckConstraint('length(surname) < 40', name='check_actors_surname_length'),
    )


__all__ = ('Actors',)
