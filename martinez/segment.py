from reprit.base import generate_repr

from .point import Point


class Segment:
    __slots__ = ('source', 'target')

    def __init__(self, source: Point, target: Point):
        self.source = source
        self.target = target

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Segment') -> bool:
        return (self.source == other.source and self.target == other.target
                if isinstance(other, Segment)
                else NotImplemented)
