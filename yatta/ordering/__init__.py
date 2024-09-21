"""Data ordering classes"""

from typing import Callable, Iterator, Sequence
from yatta.core.models import AnnotationAssignment


DataOrdering = Callable[
    [Sequence[AnnotationAssignment]], Iterator[AnnotationAssignment]
]


SequentialOrdering: DataOrdering = iter


def RandomOrdering(
    assignments: Sequence[AnnotationAssignment],
) -> Iterator[AnnotationAssignment]:
    import random

    indices = list(range(len(assignments)))
    random.shuffle(indices)
    for idx in indices:
        yield assignments[idx]
