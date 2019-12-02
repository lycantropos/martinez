from reprit.base import generate_repr

from martinez.hints import Scalar


class BoundingBox:
    __slots__ = ('_x_min', '_y_min', '_x_max', '_y_max')

    def __init__(self, x_min: Scalar, y_min: Scalar,
                 x_max: Scalar, y_max: Scalar) -> None:
        self._x_min = x_min
        self._y_min = y_min
        self._x_max = x_max
        self._y_max = y_max

    __repr__ = generate_repr(__init__)

    @property
    def x_min(self) -> Scalar:
        return self._x_min

    @property
    def y_min(self) -> Scalar:
        return self._y_min

    @property
    def x_max(self) -> Scalar:
        return self._x_max

    @property
    def y_max(self) -> Scalar:
        return self._y_max
