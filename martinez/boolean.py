import enum
from typing import Optional

from reprit.base import generate_repr

from .point import Point


class _EnumBase(enum.IntEnum):
    def __repr__(self) -> str:
        return self.__class__.__qualname__ + '.' + self.name


@enum.unique
class EdgeType(_EnumBase):
    NORMAL = 0
    NON_CONTRIBUTING = 1
    SAME_TRANSITION = 2
    DIFFERENT_TRANSITION = 3


@enum.unique
class OperationType(_EnumBase):
    INTERSECTION = 0
    UNION = 1
    DIFFERENCE = 2
    XOR = 3


@enum.unique
class PolygonType(_EnumBase):
    SUBJECT = 0
    CLIPPING = 1


class SweepEvent:
    __slots__ = ('left', 'point', 'other_event', 'polygon_type', 'edge_type')

    def __init__(self, left: bool, point: Point,
                 other_event: Optional['SweepEvent'],
                 polygon_type: PolygonType, edge_type: EdgeType) -> None:
        self.left = left
        self.point = point
        self.other_event = other_event
        self.polygon_type = polygon_type
        self.edge_type = edge_type

    __repr__ = generate_repr(__init__)
