"""Data ordering classes"""


class DataOrdering:
    """Base class for orderings

    A DataOrdering dictates what order to present data to annotators.

    This is similar to the functionality of a pytorch Sampler, but
    implementationally different.
    """

    def __init__(self, assignments):
        self.assignments = assignments

    def __len__(self):
        return len(self.assignments)

    def __iter__(self):
        raise NotImplementedError()


class SequentialOrdering(DataOrdering):
    """Present data in order"""

    def __iter__(self):
        for assignment in self.assignments:
            yield assignment


class RandomOrdering(DataOrdering):
    """Present data in random order"""

    def __iter__(self):
        import random

        indices = list(range(len(self.assignments)))
        random.shuffle(indices)
        for idx in indices:
            yield self.assignments[idx]


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
