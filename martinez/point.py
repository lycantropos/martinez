from reprit.base import generate_repr

from .hints import Scalar


class Point:
    def __init__(self, x: Scalar, y: Scalar) -> None:
        self.x = x
        self.y = y

    __repr__ = generate_repr(__init__)
