from .point import Point


class Segment:
    __slots__ = ('_source', '_target')

    def __init__(self, source: Point, target: Point):
        self._source = source
        self._target = target

    @property
    def source(self) -> Point:
        return self._source

    @property
    def target(self) -> Point:
        return self._target
