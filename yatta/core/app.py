"""
Yatta core app module.

This module handles the core functionality, including user and annotation
management.

TODO: refactor methods into separate modules so this file is easier to read.
"""

import itertools
from collections.abc import Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, Iterable, ParamSpec, Protocol, TypeVar

from sqlmodel import Session, select
from werkzeug.security import check_password_hash, generate_password_hash

from yatta.core.db import YattaDb
from yatta.core.models import AnnotationAssignment, AnnotationObject, User, UserCreate
from yatta.distributor import Distributor
from yatta.ordering import DataOrdering
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


def sliding_window(seq: Iterable, n: int):
    """Returns a sliding window (of width n) over data from the iterable"""
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


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
        ordering: DataOrdering | None = None,
        # Database settings
        db_path: str | Path = "./yatta.db",
        # Other settings
        static_files: dict[str, str | Path] | None = None,
    ) -> None:
        self.dataset = dataset
        self.task = task
        self.distributor = distributor
        self.ordering = ordering
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
        self,
        session: Session,
        exclude_users: list[int] | None = None,
        distributor: Distributor | None = None,
    ) -> None:
        if distributor is None:
            distributor = self.distributor
        if exclude_users is None:
            exclude_users = []
        users = session.exec(select(User).where(~User.id.in_(exclude_users))).all()  # type: ignore
        old_assignments = set(
            (assignment.user_id, assignment.datum_id)
            for assignment in session.exec(select(AnnotationAssignment)).all()
        )
        if distributor is None:
            raise ValueError(f"Distributor {self.distributor} not found")
        assignments = list(
            distributor(
                [user.id for user in users], [i for i, _ in enumerate(self.dataset)]
            )
        )
        assignments = [
            AnnotationAssignment(
                user_id=user_id, datum_id=index, is_complete=False, annotation=None
            )
            for user_id, index in assignments
            if (user_id, index) not in old_assignments
        ]
        session.add_all(assignments)
        session.commit()

    def assign_ordering(
        self,
        ordering: DataOrdering,
        assignments: Sequence[AnnotationAssignment],
        session: Session,
    ) -> None:
        """Assign an ordering to a list of assignments"""
        for idx, (prev, curr, next) in enumerate(
            sliding_window(itertools.chain([None], ordering(assignments), [None]), 3)
        ):
            curr.rank = idx
            curr.prev = prev.datum_id if prev is not None else None
            curr.next = next.datum_id if next is not None else None
        session.commit()

    @dbsession
    def assign_all_orderings(
        self, session: Session, ordering: DataOrdering | None = None
    ) -> None:
        ordering = ordering or self.ordering
        if ordering is None:
            raise ValueError("No ordering specified.")
        users = session.exec(select(User)).all()
        for user in users:
            assignments = session.exec(
                select(AnnotationAssignment).where(
                    AnnotationAssignment.user_id == user.id
                )
            ).all()
            self.assign_ordering(ordering, assignments, session)

    # TODO: this interface is a little messy (get and set annotations are pretty
    # asymmetric in terms of input / output). Might be worth refactoring.
    @dbsession
    def get_annotation(
        self, session: Session, user: User, datum_id: int
    ) -> AnnotationAssignment:
        annotation_assignment = session.exec(
            select(AnnotationAssignment)
            .where(AnnotationAssignment.user_id == user.id)
            .where(AnnotationAssignment.datum_id == datum_id)
        ).first()
        if not annotation_assignment:
            raise ValueError("Annotation assignment not found")
        return annotation_assignment

    @dbsession
    def set_annotation(
        self,
        session: Session,
        user: User,
        datum_id: int,
        annotation: AnnotationObject,
    ) -> AnnotationAssignment:
        annotation_assignment = self.get_annotation(user, datum_id)
        annotation_assignment.annotation = annotation.annotation
        annotation_assignment.is_complete = (
            annotation.annotation is not None and annotation.is_complete
        )
        annotation_assignment.is_skipped = annotation.is_skipped
        session.commit()
        return annotation_assignment
