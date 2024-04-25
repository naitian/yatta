"""Distributor classes"""

from itertools import product, cycle


class Distributor:
    """Base class for distributors"""

    def __init__(self, dataset):
        self.indices = list(range(len(dataset)))

    def assign(self, user_ids, indices=None):
        """Assign indices to users"""
        raise NotImplementedError()


class AllDistributor(Distributor):
    """Assign all indices to all users"""

    def assign(self, user_ids, indices=None):
        """Assign indices to users"""
        if indices is None:
            indices = self.indices
        return product(user_ids, indices)


class RoundRobinDistributor(Distributor):
    """Assigns indices in a round-robin manner."""

    def assign(self, user_ids, indices=None):
        """Assign indices to users"""
        if indices is None:
            indices = self.indices
        return zip(cycle(user_ids), indices)
