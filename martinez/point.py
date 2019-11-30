from reprit.base import generate_repr

from .hints import Scalar


class Point:
    __slots__ = ('_x', '_y')

    def __init__(self, x: Scalar, y: Scalar) -> None:
        self._x = x
        self._y = y

    __repr__ = generate_repr(__init__)

    @property
    def x(self) -> Scalar:
        return self._x

    @property
    def y(self) -> Scalar:
        return self._y
