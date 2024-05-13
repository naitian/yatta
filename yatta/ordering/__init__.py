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
