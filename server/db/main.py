from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from utils.db import get_db_url_connection


class DB(DeclarativeBase):
    __engine = create_engine(get_db_url_connection())

    @classmethod
    def get_session(cls) -> Session:
        return Session(cls.__engine)
