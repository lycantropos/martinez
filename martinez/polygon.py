from typing import List

from reprit.base import generate_repr

from .contour import Contour


class Polygon:
    __slots__ = ('_contours',)

    def __init__(self, contours: List[Contour]) -> None:
        self._contours = contours

    __repr__ = generate_repr(__init__)

    @property
    def contours(self) -> List[Contour]:
        return self._contours
