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

    def __iter__(self) -> Iterator[Point]:
        return iter(self._points)

    @property
    def points(self) -> List[Point]:
        return self._points

    @property
    def holes(self) -> List[int]:
        return self._holes

    @property
    def is_external(self) -> bool:
        return self._is_external

    @property
    def is_counterclockwise(self) -> bool:
        points = self._points
        signed_area = sum(points[index - 1].x * points[index].y
                          - points[index].x * points[index - 1].y
                          for index in range(len(points)))
        return signed_area >= 0

    def __eq__(self, other: 'Contour') -> bool:
        return (self._points == other._points
                and self._holes == other._holes
                and self._is_external is other._is_external
                if isinstance(other, Contour)
                else NotImplemented)

    def add(self, point: Point) -> None:
        self._points.append(point)

    def add_hole(self, hole: int) -> None:
        self._holes.append(hole)

    def clear_holes(self) -> None:
        self._holes.clear()