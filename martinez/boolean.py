import enum
from copy import copy
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

from prioq.base import PriorityQueue
from reprit import seekers
from reprit.base import generate_repr

from .point import Point
from .polygon import Polygon
from .segment import Segment
from .utilities import (find_intersections,
                        sign,
                        to_segments)

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
                 'edge_type', 'in_out', 'other_in_out', 'in_result',
                 'position')
    OTHER_EVENT_STATE_INDEX = 2

    def __init__(self, is_left: bool, point: Point,
                 other_event: Optional['SweepEvent'],
                 polygon_type: PolygonType,
                 edge_type: EdgeType,
                 in_out: bool = False, other_in_out: bool = False,
                 in_result: bool = False,
                 position: int = 0) -> None:
        self.is_left = is_left
        self.point = point
        self.other_event = other_event
        self.polygon_type = polygon_type
        self.edge_type = edge_type
        self.in_out = in_out
        self.other_in_out = other_in_out
        self.in_result = in_result
        self.position = position

    def __getstate__(self) -> SweepEventState:
        chain = []  # type: List[SweepEvent]
        cycle_index = self._fill_sweep_events_chain(chain)
        states = [[sweep_event.is_left, sweep_event.point, None,
                   sweep_event.polygon_type, sweep_event.edge_type,
                   sweep_event.in_out, sweep_event.other_in_out,
                   sweep_event.in_result, sweep_event.position]
                  for sweep_event in chain]
        for index in range(len(states) - 1):
            states[index][self.OTHER_EVENT_STATE_INDEX] = states[index + 1]
        if cycle_index != ACYCLIC_INDEX:
            states[-1][self.OTHER_EVENT_STATE_INDEX] = states[cycle_index]
        return states[0]

    def __setstate__(self, state: SweepEventState) -> 'SweepEvent':
        (self.is_left, self.point, self.other_event,
         self.polygon_type, self.edge_type, self.in_out,
         self.other_in_out, self.in_result,
         self.position) = (state[0], state[1], None,
                           state[3], state[4], state[5],
                           state[6], state[7], state[8])
        chain = []  # type: List[SweepEventState]
        cycle_index = self._fill_states_chain(state, chain)
        sweep_events = [self] + [SweepEvent(state[0], state[1], None,
                                            state[3], state[4], state[5],
                                            state[6], state[7], state[8])
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
                    and left.edge_type is right.edge_type
                    and left.in_out is right.in_out
                    and left.other_in_out is right.other_in_out
                    and left.in_result is right.in_result)

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
        elif self._event.point.y != other._event.point.y:
            # different points, but same x-coordinate,
            # the event with lower y-coordinate is processed first
            return self._event.point.y > other._event.point.y
        elif self._event.is_left is not other._event.is_left:
            # same point, but one is a left endpoint
            # and the other a right endpoint,
            # the right endpoint is processed first
            return self._event.is_left
        # same point, both events are left endpoints
        # or both are right endpoints
        elif sign(self._event.point, self._event.other_event.point,
                  other._event.other_event.point):  # not collinear
            # the event associate to the bottom segment is processed first
            return self._event.is_above(other._event.other_event.point)
        else:
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
        if not (sign(self.event.point, self.event.other_event.point,
                     other.event.point)
                or sign(self.event.point, self.event.other_event.point,
                        other.event.other_event.point)):
            # segments are collinear
            return (EventsQueueKey(self.event) < EventsQueueKey(other.event)
                    if self.event.polygon_type is other.event.polygon_type
                    else self.event.polygon_type < other.event.polygon_type)
        # segments are not collinear
        elif self.event.point == other.event.point:
            # same left endpoint, use the right endpoint to sort
            return self.event.is_below(other.event.other_event.point)
        # different left endpoint, use the left endpoint to sort
        elif self.event.point.x == other.event.point.x:
            return self.event.point.y < other.event.point.y
        elif EventsQueueKey(self.event) < EventsQueueKey(other.event):
            # has the line segment associated to `self` been inserted
            # into sweep line after the line segment associated to `other`?
            return other.event.is_above(self.event.point)
        else:
            # the line segment associated to `other` has been inserted
            # into sweep line after the line segment associated to `self`
            return self.event.is_below(other.event.point)


class Operation:
    __slots__ = ('_left', '_right', '_type', '_events_queue', '_resultant',
                 '_already_run')

    def __init__(self, left: Polygon, right: Polygon,
                 type_: OperationType) -> None:
        self._left = left
        self._right = right
        self._type = type_
        self._events_queue = PriorityQueue(key=EventsQueueKey,
                                           reverse=True)
        self._resultant = Polygon([])
        self._already_run = False

    __repr__ = generate_repr(__init__,
                             field_seeker=seekers.complex_)

    def __eq__(self, other: 'Operation') -> bool:
        return (self._left == other._left
                and self._right == other._right
                and self._type is other._type
                if isinstance(other, Operation)
                else NotImplemented)

    @property
    def left(self) -> Polygon:
        return self._left

    @property
    def right(self) -> Polygon:
        return self._right

    @property
    def events(self) -> List[SweepEvent]:
        events_queue = copy(self._events_queue)
        return [events_queue.pop() for _ in range(len(events_queue))]

    @property
    def resultant(self) -> Polygon:
        return self._resultant

    @property
    def type(self) -> OperationType:
        return self._type

    @property
    def is_trivial(self) -> bool:
        # test 1 for trivial result case
        if not (self._left.contours and self._right.contours):
            # at least one of the polygons is empty
            if self._type is OperationType.DIFFERENCE:
                self._resultant = self._left
            if (self._type is OperationType.UNION
                    or self._type is OperationType.XOR):
                self._resultant = (self._left
                                   if self._left.contours
                                   else self._right)
            self._already_run = True
            return True
        # test 2 for trivial result case
        left_bounding_box = self._left.bounding_box
        right_bounding_box = self._right.bounding_box
        if (left_bounding_box.x_min > right_bounding_box.x_max
                or right_bounding_box.x_min > left_bounding_box.x_max
                or left_bounding_box.y_min > right_bounding_box.y_max
                or right_bounding_box.y_min > left_bounding_box.y_max):
            # the bounding boxes do not overlap
            if self._type is OperationType.DIFFERENCE:
                self._resultant = self._left
            elif (self._type is OperationType.UNION
                  or self._type is OperationType.XOR):
                self._resultant = self._left
                self._resultant.join(self._right)
            self._already_run = True
            return True
        return False

    def divide_segment(self, event: SweepEvent, point: Point) -> None:
        # "left event" of the "right line segment"
        # resulting from dividing event.segment
        left_event = SweepEvent(True, point, event.other_event,
                                event.polygon_type,
                                EdgeType.NORMAL)
        # "right event" of the "left line segment"
        # resulting from dividing event.segment
        right_event = SweepEvent(False, point, event, event.polygon_type,
                                 EdgeType.NORMAL)
        if EventsQueueKey(left_event) < EventsQueueKey(event.other_event):
            # avoid a rounding error,
            # the left event would be processed after the right event
            event.other_event.is_left = True
            left_event.is_left = False
        event.other_event.other_event = left_event
        event.other_event = right_event
        self._events_queue.push(left_event)
        self._events_queue.push(right_event)

    def in_result(self, event: SweepEvent) -> bool:
        operation_type = self._type
        edge_type = event.edge_type
        if edge_type is EdgeType.NORMAL:
            if operation_type is OperationType.INTERSECTION:
                return not event.other_in_out
            elif operation_type is OperationType.UNION:
                return event.other_in_out
            elif operation_type is OperationType.DIFFERENCE:
                return (event.polygon_type is PolygonType.SUBJECT
                        and event.other_in_out
                        or event.polygon_type is PolygonType.CLIPPING
                        and not event.other_in_out)
            else:
                return operation_type is OperationType.XOR
        elif edge_type is EdgeType.SAME_TRANSITION:
            return (operation_type is OperationType.INTERSECTION
                    or operation_type is OperationType.UNION)
        elif edge_type is EdgeType.DIFFERENT_TRANSITION:
            return operation_type is OperationType.DIFFERENCE
        else:
            return False

    def possible_intersection(self,
                              first_event: SweepEvent,
                              second_event: SweepEvent) -> int:
        intersections_count, first_point, second_point = find_intersections(
                first_event.segment, second_event.segment)

        if not intersections_count:
            # no intersection
            return 0

        if ((intersections_count == 1) and
                (first_event.point == second_event.point or
                 (first_event.other_event.point
                  == second_event.other_event.point))):
            # the line segments intersect at an endpoint of both line segments
            return 0

        if (intersections_count == 2
                and first_event.polygon_type is second_event.polygon_type):
            raise ValueError("Edges of the same polygon should not overlap.")

        # The line segments associated to le1 and le2 intersect
        if intersections_count == 1:
            if (first_event.point != first_point
                    and first_event.other_event.point != first_point):
                # if the intersection point is not an endpoint of le1.segment
                self.divide_segment(first_event, first_point)
            if (second_event.point != first_point
                    and second_event.other_event.point != first_point):
                # if the intersection point is not an endpoint of le2.segment
                self.divide_segment(second_event, first_point)
            return 1

        # The line segments associated to le1 and le2 overlap
        sorted_events = []
        if first_event.point == second_event.point:
            sorted_events.append(None)
        elif EventsQueueKey(first_event) < EventsQueueKey(second_event):
            sorted_events.append(second_event)
            sorted_events.append(first_event)
        else:
            sorted_events.append(first_event)
            sorted_events.append(second_event)

        if first_event.other_event.point == second_event.other_event.point:
            sorted_events.append(None)
        elif (EventsQueueKey(first_event.other_event)
              < EventsQueueKey(second_event.other_event)):
            sorted_events.append(second_event.other_event)
            sorted_events.append(first_event.other_event)
        else:
            sorted_events.append(first_event.other_event)
            sorted_events.append(second_event.other_event)

        if (len(sorted_events) == 2
                or len(sorted_events) == 3 and sorted_events[2]):
            # both line segments are equal or share the left endpoint
            first_event.edge_type = EdgeType.NON_CONTRIBUTING
            second_event.edge_type = (
                EdgeType.SAME_TRANSITION
                if first_event.in_out is second_event.in_out
                else EdgeType.DIFFERENT_TRANSITION)
            if len(sorted_events) == 3:
                self.divide_segment(sorted_events[2].other_event,
                                    sorted_events[1].point)
            return 2
        if len(sorted_events) == 3:
            # the line segments share the right endpoint
            self.divide_segment(sorted_events[0], sorted_events[1].point)
            return 3

        if sorted_events[0] is not sorted_events[3].other_event:
            # no line segment includes totally the other one
            self.divide_segment(sorted_events[0], sorted_events[1].point)
            self.divide_segment(sorted_events[1], sorted_events[2].point)
            return 3

        # one line segment includes the other one
        self.divide_segment(sorted_events[0], sorted_events[1].point)
        self.divide_segment(sorted_events[3].other_event,
                            sorted_events[2].point)
        return 3

    def process_segments(self) -> None:
        for contour in self._left.contours:
            for segment in to_segments(contour.points):
                self._process_segment(segment, PolygonType.SUBJECT)
        for contour in self._right.contours:
            for segment in to_segments(contour.points):
                self._process_segment(segment, PolygonType.CLIPPING)

    def _process_segment(self, segment: Segment,
                         polygon_type: PolygonType) -> None:
        source_event = SweepEvent(True, segment.source, None, polygon_type,
                                  EdgeType.NORMAL)
        target_event = SweepEvent(True, segment.target, source_event,
                                  polygon_type, EdgeType.NORMAL)
        source_event.other_event = target_event
        if segment.min == segment.source:
            target_event.is_left = False
        else:
            source_event.is_left = False
        self._events_queue.push(source_event)
        self._events_queue.push(target_event)
