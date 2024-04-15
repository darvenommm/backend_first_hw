"""Module with DeclarativeBase class for slqAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from utils.db import get_db_url_connection


class DB(DeclarativeBase):
    """DeclarativeBase class for sqlAlchemy."""

    __engine = create_engine(get_db_url_connection())

    @classmethod
    def get_session(cls) -> Session:
        """Get session for work with the db.

        Returns:
            Session: db session.
        """
        return Session(cls.__engine)
