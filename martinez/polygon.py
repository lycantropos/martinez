from typing import List

from .contour import Contour


class Polygon:
    __slots__ = ('_contours',)

    def __init__(self, contours: List[Contour]) -> None:
        self._contours = contours

    @property
    def contours(self) -> List[Contour]:
        return self._contours
