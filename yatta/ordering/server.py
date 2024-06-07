import itertools

from sqlmodel import Session, select
from yatta.server.db import engine
from yatta.server.models import AnnotationAssignment, User
from yatta.server.settings import settings


def sliding_window(seq, n):
    """Returns a sliding window (of width n) over data from the iterable"""
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def assign_ordering(ordering, assignments, session):
    """Assign an ordering to a list of assignments"""
    for idx, (prev, curr, next) in enumerate(
        sliding_window(itertools.chain([None], ordering(assignments), [None]), 3)
    ):
        curr.rank = idx
        curr.prev = prev.datum_id if prev is not None else None
        curr.next = next.datum_id if next is not None else None
    session.commit()


def assign_all_orderings():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        for user in users:
            assignments = session.exec(
                select(AnnotationAssignment).where(
                    AnnotationAssignment.user_id == user.id
                )
            ).all()
            assign_ordering(settings.ordering, assignments, session)
