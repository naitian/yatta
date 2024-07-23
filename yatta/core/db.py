from pathlib import Path
from typing import Any, Generator

from sqlmodel import Session, SQLModel, create_engine

from yatta.core.models import *  # noqa


class YattaDb:
    def __init__(self, db_path: str | Path, connect_args: dict[str, Any] | None = None):
        if isinstance(db_path, str):
            db_path = Path(db_path)
        self.connect_args = connect_args or {"check_same_thread": False}
        self.database = "sqlite:///" + str(db_path.resolve())
        self.engine = create_engine(
            self.database, echo=False, connect_args=self.connect_args
        )

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session
