import enum
from functools import (partial,
                       partialmethod)
from operator import (attrgetter,
                      itemgetter)
from reprlib import recursive_repr
from typing import (Callable,
                    List,
                    Optional,
                    TypeVar,
                    Union)

from reprit.base import generate_repr

from .point import Point
from .segment import Segment
from .utilities import sign

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


Domain = TypeVar('Domain')


def _fill_chain(start: Domain, chain: List[Domain],
                to_next: Callable[[Domain], Optional[Domain]]) -> int:
    chain.append(start)
    cursor = to_next(start)
    while cursor is not None:
        try:
            cycle_index = next(index
                               for index, element in enumerate(chain)
                               if element is cursor)
        except StopIteration:
            chain.append(cursor)
            cursor = to_next(cursor)
        else:
            # last element points to already visited one
            # with this index
            return cycle_index
    # has no cycles
    return ACYCLIC_INDEX


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
        cycle_index = self._fill_sweep_events_chain(chain)
        states = [[sweep_event.is_left, sweep_event.point, None,
                   sweep_event.polygon_type, sweep_event.edge_type]
                  for sweep_event in chain]
        for index in range(len(states) - 1):
            states[index][self.OTHER_EVENT_STATE_INDEX] = states[index + 1]
        if cycle_index != ACYCLIC_INDEX:
            states[-1][self.OTHER_EVENT_STATE_INDEX] = states[cycle_index]
        return states[0]

    def __setstate__(self, state: SweepEventState) -> 'SweepEvent':
        (self.is_left, self.point, self.other_event,
         self.polygon_type, self.edge_type) = (state[0], state[1], None,
                                               state[3], state[4])
        chain = []  # type: List[SweepEventState]
        cycle_index = self._fill_states_chain(state, chain)
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
                and (self._fill_sweep_events_chain(chain)
                     == other._fill_sweep_events_chain(other_chain))
                and len(chain) == len(other_chain)
                and all(are_fields_equal(child, other_child)
                        for child, other_child in zip(chain[1:],
                                                      other_chain[1:]))
                if isinstance(other, SweepEvent)
                else NotImplemented)

    _fill_sweep_events_chain = partialmethod(_fill_chain,
                                             to_next=attrgetter('other_event'))
    _fill_states_chain = staticmethod(
            partial(_fill_chain,
                    to_next=itemgetter(OTHER_EVENT_STATE_INDEX)))

    @property
    def is_vertical(self) -> bool:
        self.validate()
        return self.point.x == self.other_event.point.x

    @property
    def segment(self) -> Segment:
        self.validate()
        return Segment(self.point, self.other_event.point)

    def is_above(self, point: Point) -> bool:
        return not self.is_below(point)

    def is_below(self, point: Point) -> bool:
        self.validate()
        return (sign(self.point, self.other_event.point, point) == 1
                if self.is_left
                else sign(self.other_event.point, self.point, point) == 1)

    def validate(self) -> None:
        if self.other_event is None:
            raise ValueError('No "other_event" found.')


class EventsQueueKey:
    __slots__ = ('_event',)

    def __init__(self, event: SweepEvent) -> None:
        self._event = event

    __repr__ = generate_repr(__init__)

    @property
    def event(self) -> SweepEvent:
        return self._event

    def __eq__(self, other: 'EventsQueueKey') -> bool:
        return (self._event == other._event
                if isinstance(other, EventsQueueKey)
                else NotImplemented)

    def __lt__(self, other: 'EventsQueueKey') -> bool:
        if not isinstance(other, EventsQueueKey):
            return NotImplemented
        if self._event.point.x != other._event.point.x:
            # different x-coordinate,
            # the event with lower x-coordinate is processed first
            return self._event.point.x > other._event.point.x
        if self._event.point.y != other._event.point.y:
            # different points, but same x-coordinate,
            # the event with lower y-coordinate is processed first
            return self._event.point.y > other._event.point.y
        if self._event.is_left is not other._event.is_left:
            # same point, but one is a left endpoint
            # and the other a right endpoint,
            # the right endpoint is processed first
            return self._event.is_left
        # same point, both events are left endpoints
        # or both are right endpoints
        if sign(self._event.point, self._event.other_event.point,
                other._event.other_event.point):  # not collinear
            # the event associate to the bottom segment is processed first
            return self._event.is_above(other._event.other_event.point)
        return self._event.polygon_type > other._event.polygon_type


class SweepLineKey:
    __slots__ = ('_event',)

    def __init__(self, event: SweepEvent) -> None:
        self._event = event

    __repr__ = generate_repr(__init__)

    @property
    def event(self) -> SweepEvent:
        return self._event

    def __eq__(self, other: 'SweepLineKey') -> bool:
        return (self._event == other._event
                if isinstance(other, SweepLineKey)
                else NotImplemented)

    def __lt__(self, other: 'SweepLineKey') -> bool:
        if not isinstance(other, SweepLineKey):
            return NotImplemented
        if self is other:
            return False
        if (sign(self.event.point, self.event.other_event.point,
                 other.event.point)
                or sign(self.event.point, self.event.other_event.point,
                        other.event.other_event.point)):
            # segments are not collinear
            if self.event.point == other.event.point:
                # same left endpoint, use the right endpoint to sort
                return self.event.is_below(other.event.other_event.point)
            # different left endpoint, use the left endpoint to sort
            elif self.event.point.x == other.event.point.x:
                return self.event.point.y < other.event.point.y
            elif EventsQueueKey(self.event) < EventsQueueKey(other.event):
                # has the line segment associated to `self` been inserted
                # into sweep line after the line segment associated to `other`?
                return other.event.is_above(self.event.point)
            # the line segment associated to `other` has been inserted
            # into sweep line after the line segment associated to `self`
            return self.event.is_below(other.event.point)
        # segments are collinear
        return (self.event.polygon_type < other.event.polygon_type
                if self.event.polygon_type is not other.event.polygon_type
                else EventsQueueKey(self.event) < EventsQueueKey(other.event))
