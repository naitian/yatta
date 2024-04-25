from sqlmodel import Session, SQLModel, create_engine

from yatta.server.models import *  # noqa
from yatta.server.settings import settings

connect_args = {"check_same_thread": False}
engine = create_engine(settings.database, echo=False, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
