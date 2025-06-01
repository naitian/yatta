"""
Yatta core app module.

This module handles the core functionality, including user and annotation
management.

TODO: refactor methods into separate modules so this file is easier to read.
"""

from collections import OrderedDict
import itertools
from collections.abc import Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    Mapping,
    ParamSpec,
    Protocol,
    TypeVar,
)

from pydantic import ValidationError
from sqlmodel import Session, select
from werkzeug.security import check_password_hash, generate_password_hash

from yatta.core.db import YattaDb
from yatta.core.models import AnnotationAssignment, AnnotationObject, User, UserCreate
from yatta.core.plugins import Component
from yatta.distributor import Distributor
from yatta.ordering import DataOrdering

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
        task: Mapping[str, Component] = {},
        distributor: Distributor | None = None,
        ordering: DataOrdering | None = None,
        # Database settings
        db_path: str | Path = "./yatta.db",
        # Other settings
        static_files: dict[str, str | Path] | None = None,
        # TODO: better typing for hooks
        hooks: dict[str, Callable | list[Callable]] | None = None,
    ) -> None:
        self.dataset = dataset
        self.task: OrderedDict = OrderedDict(task)
        self.distributor = distributor
        self.ordering = ordering
        self.static_files = static_files
        self.hooks = hooks or {}

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

    def add_hook(self, hook_name: str, hook: Callable) -> None:
        """
        Add a hook to the Yatta app.

        Args:
            hook_name: The name of the hook.
            hook: The hook function to add.
        """
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        hook_obj = self.hooks[hook_name]
        if isinstance(hook_obj, list):
            hook_obj.append(hook)
        elif callable(hook_obj):
            self.hooks[hook_name] = [hook_obj, hook]
        if not callable(hook):
            raise TypeError(f"Hook {hook_name} must be callable, got {type(hook)}")

    def call_hooks(
        self,
        hooks: dict[str, Callable | list[Callable]],
        hook_name: str,
        *args,
        **kwargs,
    ):
        """
        Call hooks registered in the Yatta app.

        Args:
            hooks: A dictionary of hooks.
            hook_name: The name of the hook to call.
            *args: Positional arguments to pass to the hook
            **kwargs: Keyword arguments to pass to the hook
        """
        if hook_name in hooks:
            hook_obj = hooks[hook_name]
            if isinstance(hook_obj, list):
                for hook in hook_obj:
                    hook(yatta=self, *args, **kwargs)
            elif callable(hook_obj):
                hook_obj(yatta=self, *args, **kwargs)
            else:
                raise TypeError(f"Hook {hook_name} is not callable")

    @dbsession
    def add_user(self, session: Session, user: UserCreate) -> User:
        self.call_hooks(self.hooks, "before_add_user", user=user)

        hashed_password = generate_password_hash(user.password)
        db_user = User.model_validate(user, update={"hashed_password": hashed_password})

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        self.call_hooks(self.hooks, "after_add_user", user=db_user)

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
        # FIXME: This method does not remove old assignments. Old assignments
        # should be removed or deactivated.
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
        try:
            annotation_assignment = self.get_annotation(user, datum_id)
            annotation_assignment.annotation = annotation.annotation
            annotation_assignment.is_complete = (
                annotation.annotation is not None and annotation.is_complete
            )
            annotation_assignment.is_skipped = annotation.is_skipped
            session.commit()
            return annotation_assignment
        except ValidationError as e:
            session.rollback()
            raise e

    # TODO: make a response model for this
    def get_task(self) -> dict[str, Any]:
        return {
            "task": [
                {
                    "field": key,
                    "component": component.get_props(),
                }
                for key, component in self.task.items()
            ],
            "components": self.aggregate_component_names(self.task),
        }

    def aggregate_component_names(self, task):
        """
        task is a dict with keys as the field names and values as the components,
        which have a name attribute

        for now, we ignore components with children; we can add this later

        return a dict component.name -> component
        """
        return {
            component.name: component.get_definition() for component in task.values()
        }
