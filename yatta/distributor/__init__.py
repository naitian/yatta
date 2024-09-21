"""Distributor classes"""

from itertools import cycle, product
from typing import Callable, Iterator, Sequence, Tuple

Distributor = Callable[[Sequence[int], Sequence[int]], Iterator[Tuple[int, int]]]


AllDistributor: Distributor = product


def RoundRobinDistributor(user_ids, indices):
    return zip(cycle(user_ids), indices)
