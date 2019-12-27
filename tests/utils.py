import pickle
from typing import (Any,
                    Hashable,
                    Iterable,
                    List,
                    Sequence,
                    Tuple,
                    TypeVar,
                    Union)

from _martinez import (BoundingBox as BoundBoundingBox,
                       Contour as BoundContour,
                       EventsQueueKey as BoundEventsQueueKey,
                       Operation as BoundOperation,
                       Point as BoundPoint,
                       Polygon as BoundPolygon,
                       Segment as BoundSegment,
                       SweepEvent as BoundSweepEvent,
                       SweepLineKey as BoundSweepLineKey,
                       find_intersections as bound_find_intersections)
from hypothesis import strategies
from hypothesis.strategies import SearchStrategy

from martinez.boolean import (EventsQueueKey as PortedEventsQueueKey,
                              Operation as PortedOperation,
                              SweepEvent as PortedSweepEvent,
                              SweepLineKey as PortedSweepLineKey)
from martinez.bounding_box import BoundingBox as PortedBoundingBox
from martinez.contour import Contour as PortedContour
from martinez.hints import Scalar
from martinez.point import Point as PortedPoint
from martinez.polygon import Polygon as PortedPolygon
from martinez.segment import Segment as PortedSegment
from martinez.utilities import (
    find_intersections as ported_find_intersections,
    sign)

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


def transpose(sequence: Sequence[Tuple[Domain, ...]]
              ) -> Tuple[Sequence[Domain], ...]:
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


def to_valid_coordinates(pair: Tuple[Scalar, Scalar]) -> Tuple[Scalar, Scalar]:
    start, end = pair
    if end - start < 1:
        start = end - 10
    elif end - start > 100:
        end = start + 10
    return start, end


def pickle_round_trip(object_: Domain) -> Domain:
    return pickle.loads(pickle.dumps(object_))


def vertices_form_strict_polygon(vertices: Sequence[Union[PortedPoint,
                                                          BoundPoint]]
                                 ) -> bool:
    return all(sign(vertices[index - 1],
                    vertices[index],
                    vertices[(index + 1) % len(vertices)])
               for index in range(len(vertices)))


def strategy_to_pairs(strategy: Strategy[Domain]
                      ) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(strategy, strategy)


def is_bounding_box_empty(bounding_box: Union[BoundBoundingBox,
                                              PortedBoundingBox]) -> bool:
    return not (bounding_box.x_min or bounding_box.y_min
                or bounding_box.x_max or bounding_box.y_max)


AnySweepEvent = TypeVar('AnySweepEvent', BoundSweepEvent, PortedSweepEvent)


def is_sweep_event_non_degenerate(event: AnySweepEvent) -> bool:
    return not event.segment.is_degenerate


def are_non_overlapping_sweep_events_pair(events_pair: Tuple[AnySweepEvent,
                                                             AnySweepEvent]
                                          ) -> bool:
    first_event, second_event = events_pair
    first_segment, second_segment = first_event.segment, second_event.segment
    if isinstance(first_event, BoundSweepEvent):
        intersections_count = bound_find_intersections(first_segment,
                                                       second_segment)[0]
    else:
        intersections_count = ported_find_intersections(first_segment,
                                                        second_segment)[0]
    return intersections_count != 2


def are_sweep_events_pair_with_different_polygon_types(
        events_pair: Tuple[AnySweepEvent, AnySweepEvent]) -> bool:
    first_event, second_event = events_pair
    return first_event.polygon_type != second_event.polygon_type


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


traverse_sweep_event = PortedSweepEvent._traverse


def are_bound_ported_sweep_events_equal(bound: BoundSweepEvent,
                                        ported: PortedSweepEvent) -> bool:
    def are_fields_equal(bound: BoundSweepEvent,
                         ported: PortedSweepEvent) -> bool:
        return (bound.is_left is ported.is_left
                and are_bound_ported_points_equal(bound.point, ported.point)
                and bound.polygon_type == ported.polygon_type
                and bound.edge_type == ported.edge_type
                and bound.in_out is ported.in_out
                and bound.other_in_out is ported.other_in_out
                and bound.in_result is ported.in_result
                and bound.result_in_out is ported.result_in_out
                and bound.position == ported.position
                and bound.contour_id == ported.contour_id)

    bound_left_links, ported_left_links = {}, {}
    bound_right_links, ported_right_links = {}, {}
    bound_events = traverse_sweep_event(bound, bound_left_links,
                                        bound_right_links)
    ported_events = traverse_sweep_event(ported, ported_left_links,
                                         ported_right_links)
    return (bound_left_links == ported_left_links
            and bound_right_links == ported_right_links
            and len(bound_events) == len(ported_events)
            and all(map(are_fields_equal, bound_events, ported_events)))


def are_bound_ported_sweep_events_lists_equal(bound: List[BoundSweepEvent],
                                              ported: List[PortedSweepEvent]
                                              ) -> bool:
    return (len(bound) == len(ported)
            and all(map(are_bound_ported_sweep_events_equal, bound, ported)))


def are_bound_ported_events_queue_keys_equal(bound: BoundEventsQueueKey,
                                             ported: PortedEventsQueueKey
                                             ) -> bool:
    return are_bound_ported_sweep_events_equal(bound.event, ported.event)


def are_bound_ported_sweep_line_keys_equal(bound: BoundSweepLineKey,
                                           ported: PortedSweepLineKey
                                           ) -> bool:
    return are_bound_ported_sweep_events_equal(bound.event, ported.event)


def are_bound_ported_operations_equal(bound: BoundOperation,
                                      ported: PortedOperation) -> bool:
    return (are_bound_ported_polygons_equal(bound.left, ported.left)
            and are_bound_ported_polygons_equal(bound.right, ported.right)
            and bound.type == ported.type)
