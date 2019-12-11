import enum
from typing import (List,
                    Optional)

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
        if self is other:
            return True

        def are_fields_equal(left: SweepEvent, right: SweepEvent) -> bool:
            return (left.is_left is right.is_left
                    and left.point == right.point
                    and left.polygon_type is right.polygon_type
                    and left.edge_type is right.edge_type)

        children, other_children = [], []
        return (are_fields_equal(self, other)
                and (self._fill_children(children)
                     == other._fill_children(other_children))
                and all(are_fields_equal(child, other_child)
                        for child, other_child in zip(children,
                                                      other_children))
                if isinstance(other, SweepEvent)
                else NotImplemented)

    def _fill_children(self, children: List['SweepEvent']) -> int:
        cursor = self.other_event
        while cursor is not None:
            try:
                cycle_index = next(index
                                   for index, child in enumerate(children)
                                   if child is cursor)
            except StopIteration:
                children.append(cursor)
                cursor = cursor.other_event
            else:
                # last child points to already visited one
                # with this index
                return cycle_index
        # has no cycles
        return -1

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
