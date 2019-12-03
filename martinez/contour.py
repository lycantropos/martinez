from typing import (Iterator,
                    List)

from reprit.base import generate_repr

from .point import Point


class Contour:
    __slots__ = ('_points', '_holes', '_is_external')

    def __init__(self, points: List[Point], holes: List[int], is_external: bool
                 ) -> None:
        self._points = points
        self._holes = holes
        self._is_external = is_external

    __repr__ = generate_repr(__init__)

    @property
    def points(self) -> List[Point]:
        return self._points

    @property
    def holes(self) -> List[int]:
        return self._holes

    @property
    def is_external(self) -> bool:
        return self._is_external
