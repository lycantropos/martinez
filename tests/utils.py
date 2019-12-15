import pickle
from typing import (Any,
                    Hashable,
                    Iterable,
                    Sequence,
                    Tuple,
                    TypeVar,
                    Union)

from _martinez import (BoundingBox as BoundBoundingBox,
                       Contour as BoundContour,
                       EventsQueueKey as BoundEventsQueueKey,
                       Point as BoundPoint,
                       Polygon as BoundPolygon,
                       Segment as BoundSegment,
                       SweepEvent as BoundSweepEvent,
                       SweepLineKey as BoundSweepLineKey)
from hypothesis.strategies import SearchStrategy

from martinez.boolean import (EventsQueueKey as PortedEventsQueueKey,
                              SweepEvent as PortedSweepEvent,
                              SweepLineKey as PortedSweepLineKey)
from martinez.bounding_box import BoundingBox as PortedBoundingBox
from martinez.contour import Contour as PortedContour
from martinez.point import Point as PortedPoint
from martinez.polygon import Polygon as PortedPolygon
from martinez.segment import Segment as PortedSegment
from martinez.utilities import sign

Domain = TypeVar('Domain')
Strategy = SearchStrategy
BoundPointsPair = Tuple[BoundPoint, BoundPoint]
BoundPointsTriplet = Tuple[BoundPoint, BoundPoint, BoundPoint]
PortedPointsPair = Tuple[PortedPoint, PortedPoint]
PortedPointsTriplet = Tuple[PortedPoint, PortedPoint, PortedPoint]
BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSweepEventsPair = Tuple[BoundSweepEvent, PortedSweepEvent]


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


FirstCoordinate = TypeVar('FirstCoordinate')
SecondCoordinate = TypeVar('SecondCoordinate')


def transpose(sequence: Sequence[Tuple[FirstCoordinate, SecondCoordinate]]
              ) -> Tuple[Sequence[FirstCoordinate],
                         Sequence[SecondCoordinate]]:
    sequence_type = type(sequence)
    if not sequence:
        return sequence_type(), sequence_type()
    return tuple(map(sequence_type, zip(*sequence)))


def capacity(iterable: Iterable[Any]) -> int:
    return sum(1 for _ in iterable)


def all_unique(iterable: Iterable[Hashable]) -> bool:
    seen = set()
    for element in iterable:
        if element not in seen:
            seen.add(element)
        else:
            return False
    return True


def permute(sequence: Sequence[Domain],
            permutation: Sequence[int]) -> Iterable[Domain]:
    return map(sequence.__getitem__, permutation)


def is_even_permutation(permutation: Sequence[int]) -> bool:
    counter = 0
    for index in range(len(permutation)):
        for next_index in range(index + 1, len(permutation)):
            if permutation[index] > permutation[next_index]:
                counter += 1
    return not counter % 2


def pickle_round_trip(object_: Domain) -> Domain:
    return pickle.loads(pickle.dumps(object_))


def vertices_form_strict_polygon(vertices: Sequence[Union[PortedPoint,
                                                          BoundPoint]]
                                 ) -> bool:
    return all(sign(vertices[index - 1],
                    vertices[index],
                    vertices[(index + 1) % len(vertices)])
               for index in range(len(vertices)))


def are_bound_ported_bounding_boxes_equal(bound: BoundBoundingBox,
                                          ported: PortedBoundingBox) -> bool:
    return (bound.x_min == ported.x_min and bound.y_min == ported.y_min
            and bound.x_max == ported.x_max and bound.y_max == ported.y_max)


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def are_bound_ported_points_sequences_equal(bound: Sequence[BoundPoint],
                                            ported: Sequence[PortedPoint]
                                            ) -> bool:
    return (len(bound) == len(ported)
            and all(map(are_bound_ported_points_equal, bound, ported)))


def are_bound_ported_segments_equal(bound: BoundSegment,
                                    ported: PortedSegment) -> bool:
    return (are_bound_ported_points_equal(bound.source, ported.source)
            and are_bound_ported_points_equal(bound.target, ported.target))


def is_bounding_box_empty(bounding_box: Union[BoundBoundingBox,
                                              PortedBoundingBox]) -> bool:
    return not (bounding_box.x_min or bounding_box.y_min
                or bounding_box.x_max or bounding_box.y_max)


def are_bound_ported_contours_equal(bound: BoundContour,
                                    ported: PortedContour) -> bool:
    return (are_bound_ported_points_sequences_equal(bound.points,
                                                    ported.points)
            and bound.holes == ported.holes
            and bound.is_external is ported.is_external)


def are_bound_ported_polygons_equal(bound: BoundPolygon,
                                    ported: PortedPolygon) -> bool:
    return all(map(are_bound_ported_contours_equal,
                   bound.contours, ported.contours))


def to_sweep_event_children_count(sweep_event: Union[BoundSweepEvent,
                                                     PortedSweepEvent]) -> int:
    children_ids = set()
    cursor = sweep_event
    while (cursor.other_event is not None
           and cursor.other_event is not sweep_event):
        sweep_event = cursor.other_event
        sweep_event_id = id(cursor)
        if sweep_event_id in children_ids:
            break
        children_ids.add(sweep_event_id)
    return len(children_ids)


fill_sweep_events_chain = PortedSweepEvent._fill_sweep_events_chain


def are_bound_ported_sweep_events_equal(bound: BoundSweepEvent,
                                        ported: PortedSweepEvent) -> bool:
    bound_children_count = to_sweep_event_children_count(bound)
    ported_children_count = to_sweep_event_children_count(ported)
    if bound_children_count != ported_children_count:
        return False

    def are_fields_equal(bound: BoundSweepEvent,
                         ported: PortedSweepEvent) -> bool:
        return (bound.is_left is ported.is_left
                and are_bound_ported_points_equal(bound.point, ported.point)
                and bound.polygon_type == ported.polygon_type
                and bound.edge_type == ported.edge_type)

    if not are_fields_equal(bound, ported):
        return False
    bound_chain, ported_chain = [], []
    bound_cycle_index = fill_sweep_events_chain(bound, bound_chain)
    ported_cycle_index = fill_sweep_events_chain(ported, ported_chain)
    if bound_cycle_index != ported_cycle_index:
        return False
    return (len(bound_chain) == len(ported_chain)
            and all(map(are_fields_equal, bound_chain[1:], ported_chain[1:])))


def are_bound_ported_events_queue_keys_equal(bound: BoundEventsQueueKey,
                                             ported: PortedEventsQueueKey
                                             ) -> bool:
    return are_bound_ported_sweep_events_equal(bound.event, ported.event)


def are_bound_ported_sweep_line_keys_equal(bound: BoundSweepLineKey,
                                           ported: PortedSweepLineKey
                                           ) -> bool:
    return are_bound_ported_sweep_events_equal(bound.event, ported.event)
