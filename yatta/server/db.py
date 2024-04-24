from sqlmodel import Field, Session, SQLModel, create_engine

from yatta.server.settings import settings


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    _password: str


connect_args = {"check_same_thread": False}
engine = create_engine(settings.database, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
