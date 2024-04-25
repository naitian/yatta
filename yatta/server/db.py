from sqlmodel import Field, Session, SQLModel, create_engine

from yatta.server.settings import settings
from yatta.server.models import User


connect_args = {"check_same_thread": False}
engine = create_engine(settings.database, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
