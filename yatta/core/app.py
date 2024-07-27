"""
Yatta core app module.

This module handles the core functionality, including user and annotation
management.

TODO: refactor methods into separate modules so this file is easier to read.
"""

from collections.abc import Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, ParamSpec, Protocol, TypeVar

from sqlmodel import Session, select
from werkzeug.security import check_password_hash, generate_password_hash

from yatta.core.db import YattaDb
from yatta.core.models import AnnotationAssignment, User, UserCreate
from yatta.distributor import Distributor
from yatta.server.plugins import Component

P = ParamSpec("P")
R = TypeVar("R", covariant=True)


class DbFunction(Protocol[P, R]):
    """Type for yatta methods that require a db session."""

    def __call__(
        _,  # type:ignore to mute self warning
        self: Any,
        session: Session,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R: ...


def dbsession(func: DbFunction[P, R]):
    """Method decorator to inject a db session.add()."""

    def wrapper(self: "Yatta", *args: P.args, **kwargs: P.kwargs) -> R:
        if self._session is None:
            raise RuntimeError("No session found. Use `with app.session():`")
        return func(self, self._session, *args, **kwargs)

    return wrapper


class Yatta:
    def __init__(
        self,
        # Yatta settings
        dataset: Sequence,
        task: dict[str, Component] | None = None,
        distributor: Distributor | None = None,
        # Database settings
        db_path: str | Path = "./yatta.db",
        # Other settings
        static_files: dict[str, str | Path] | None = None,
    ) -> None:
        self.dataset = dataset
        self.task = task
        self.distributor = distributor
        self.static_files = static_files

        self.db = YattaDb(db_path=db_path)
        self.init_db()

    def init_db(self) -> None:
        """Initialize the database."""
        self.db.create_db_and_tables()
        self._session = None

    @contextmanager
    def session(self) -> Generator[None, None, None]:
        try:
            self._session = Session(self.db.engine)
            yield
        finally:
            if self._session is not None:
                self._session.close()
                self._session = None

    @dbsession
    def add_user(self, session: Session, user: UserCreate) -> User:
        hashed_password = generate_password_hash(user.password)
        db_user = User.model_validate(user, update={"hashed_password": hashed_password})

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @dbsession
    def get_user(self, session: Session, username: str) -> User:
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise ValueError(f"User {username} not found.")
        return user

    @dbsession
    def make_admin(self, session: Session, user: User) -> User:
        user.is_admin = True
        session.commit()
        session.refresh(user)
        return user

    @dbsession
    def authenticate_user(self, session: Session, username: str, password: str) -> User:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user or not check_password_hash(user.hashed_password, password):
            raise ValueError("Invalid username or password")
        return user

    @dbsession
    def list_users(self, session: Session) -> list[User]:
        return list(session.exec(select(User)).all())

    @dbsession
    def assign_tasks(
        self, session: Session, exclude_users: list[User] | None = None
    ) -> None:
        if exclude_users is None:
            exclude_users = []
        users = session.exec(
            select(User).where(~User.username.in_(exclude_users))
        ).all()
        old_assignments = set(
            (assignment.user_id, assignment.datum_id)
            for assignment in session.exec(select(AnnotationAssignment)).all()
        )
        if self.distributor is None:
            raise ValueError(f"Distributor {self.distributor} not found")
        assignments = list(self.distributor.assign([user.id for user in users]))
        assignments = [
            AnnotationAssignment(
                user_id=user_id, datum_id=index, is_complete=False, annotation=None
            )
            for user_id, index in assignments
            if (user_id, index) not in old_assignments
        ]
        session.add_all(assignments)
        session.commit()
