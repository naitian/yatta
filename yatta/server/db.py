import os

from sqlmodel import Session, SQLModel, create_engine

from yatta.server.models import *  # noqa
from yatta.server.settings import settings

connect_args = {"check_same_thread": False}
database = "sqlite:///" + os.path.join(os.getcwd(), settings.db_name) if settings.database is None else settings.database
engine = create_engine(database, echo=False, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
