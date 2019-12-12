import enum
from reprlib import recursive_repr
from typing import (List,
                    Optional,
                    Union)

from reprit.base import generate_repr

from .point import Point
from .segment import Segment

ACYCLIC_INDEX = -1


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


SweepEventState = List[Union[bool, Point, Optional[list],
                             PolygonType, EdgeType]]


class SweepEvent:
    __slots__ = ('is_left', 'point', 'other_event', 'polygon_type',
                 'edge_type')
    OTHER_EVENT_STATE_INDEX = 2

    def __init__(self, is_left: bool, point: Point,
                 other_event: Optional['SweepEvent'],
                 polygon_type: PolygonType, edge_type: EdgeType) -> None:
        self.is_left = is_left
        self.point = point
        self.other_event = other_event
        self.polygon_type = polygon_type
        self.edge_type = edge_type

    def __getstate__(self) -> SweepEventState:
        chain = []  # type: List[SweepEvent]
        cycle_index = self._fill_chain(chain)
        states = [[sweep_event.is_left, sweep_event.point, None,
                   sweep_event.polygon_type, sweep_event.edge_type]
                  for sweep_event in chain]
        for index in range(len(states) - 1):
            states[index][self.OTHER_EVENT_STATE_INDEX] = states[index + 1]
        if cycle_index != ACYCLIC_INDEX:
            states[-1][self.OTHER_EVENT_STATE_INDEX] = states[cycle_index]
        return states[0]

    def __setstate__(self, state: SweepEventState) -> 'SweepEvent':
        chain = []  # type: List[SweepEventState]
        cycle_index = self._fill_states_chain(state, chain)
        (self.is_left, self.point, self.other_event,
         self.polygon_type, self.edge_type) = (state[0], state[1], None,
                                               state[3], state[4])
        sweep_events = [self] + [SweepEvent(state[0], state[1], None,
                                            state[3], state[4])
                                 for state in chain[1:]]
        for index in range(len(sweep_events) - 1):
            sweep_events[index].other_event = sweep_events[index + 1]
        if cycle_index != ACYCLIC_INDEX:
            sweep_events[-1].other_event = sweep_events[cycle_index]

    __repr__ = recursive_repr()(generate_repr(__init__))

    def __eq__(self, other: 'SweepEvent') -> bool:
        if self is other:
            return True

        def are_fields_equal(left: SweepEvent, right: SweepEvent) -> bool:
            return (left.is_left is right.is_left
                    and left.point == right.point
                    and left.polygon_type is right.polygon_type
                    and left.edge_type is right.edge_type)

        chain, other_chain = [], []
        return (are_fields_equal(self, other)
                and self._fill_chain(chain) == other._fill_chain(other_chain)
                and len(chain) == len(other_chain)
                and all(are_fields_equal(child, other_child)
                        for child, other_child in zip(chain[1:],
                                                      other_chain[1:]))
                if isinstance(other, SweepEvent)
                else NotImplemented)

    def _fill_chain(self, chain: List['SweepEvent']) -> int:
        chain.append(self)
        cursor = self.other_event
        while cursor is not None:
            try:
                cycle_index = next(index
                                   for index, element in enumerate(chain)
                                   if element is cursor)
            except StopIteration:
                chain.append(cursor)
                cursor = cursor.other_event
            else:
                # last child points to already visited one
                # with this index
                return cycle_index
        # has no cycles
        return ACYCLIC_INDEX

    @classmethod
    def _fill_states_chain(cls, state: SweepEventState,
                           chain: List[SweepEventState]) -> int:
        chain.append(state)
        cursor = state[cls.OTHER_EVENT_STATE_INDEX]
        while cursor is not None:
            try:
                cycle_index = next(index
                                   for index, child in enumerate(chain)
                                   if child is cursor)
            except StopIteration:
                chain.append(cursor)
                cursor = cursor[cls.OTHER_EVENT_STATE_INDEX]
            else:
                # last child points to already visited one
                # with this index
                return cycle_index
        # has no cycles
        return ACYCLIC_INDEX

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
