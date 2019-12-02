from operator import attrgetter

from reprit.base import generate_repr

from .point import Point

points_key = attrgetter('x', 'y')


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

    @property
    def max(self) -> Point:
        return max(self.source, self.target,
                   key=points_key)

    @property
    def min(self) -> Point:
        return min(self.source, self.target,
                   key=points_key)

    @property
    def is_degenerate(self) -> bool:
        return self.source == self.target

    @property
    def is_vertical(self) -> bool:
        return self.source.x == self.target.x

    @property
    def reversed(self) -> 'Segment':
        return Segment(self.target, self.source)
