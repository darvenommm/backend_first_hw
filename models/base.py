from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from helpers.db import get_db_url_connection


class Base(DeclarativeBase):
    pass


engine = create_engine(get_db_url_connection())

def get_session() -> Session:
    return Session(engine)


__all__ = ('Base', 'get_session')
