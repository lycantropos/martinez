import enum
from typing import Optional

from reprit.base import generate_repr

from .point import Point
from .segment import Segment


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
    __slots__ = ('is_left', 'point', 'other_event', 'polygon_type',
                 'edge_type')

    def __init__(self, is_left: bool, point: Point,
                 other_event: Optional['SweepEvent'],
                 polygon_type: PolygonType, edge_type: EdgeType) -> None:
        self.is_left = is_left
        self.point = point
        self.other_event = other_event
        self.polygon_type = polygon_type
        self.edge_type = edge_type

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'SweepEvent') -> bool:
        return (self.is_left is other.is_left
                and self.point == other.point
                and self.other_event == other.other_event
                and self.polygon_type is other.polygon_type
                and self.edge_type is other.edge_type
                if isinstance(other, SweepEvent)
                else NotImplemented)

    @property
    def is_vertical(self) -> bool:
        self.validate()
        return self.point.x == self.other_event.point.x

    @property
    def segment(self) -> Segment:
        self.validate()
        return Segment(self.point, self.other_event.point)

    def validate(self) -> None:
        if self.other_event is None:
            raise ValueError('No "other_event" found.')
