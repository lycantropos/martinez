from reprit.base import generate_repr

from .point import Point


class Segment:
    __slots__ = ('_source', '_target')

    def __init__(self, source: Point, target: Point):
        self._source = source
        self._target = target

    __repr__ = generate_repr(__init__)

    @property
    def source(self) -> Point:
        return self._source

    @property
    def target(self) -> Point:
        return self._target

    def __eq__(self, other: 'Segment') -> bool:
        return (self._source == other._source and self._target == other._target
                if isinstance(other, Segment)
                else NotImplemented)
