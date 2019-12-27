import math
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
    to_segments as to_ported_segments)

Domain = TypeVar('Domain')
Strategy = SearchStrategy
BoundPointsPair = Tuple[BoundPoint, BoundPoint]
BoundPointsTriplet = Tuple[BoundPoint, BoundPoint, BoundPoint]
PortedPointsPair = Tuple[PortedPoint, PortedPoint]
PortedPointsTriplet = Tuple[PortedPoint, PortedPoint, PortedPoint]
BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSweepEventsPair = Tuple[BoundSweepEvent, PortedSweepEvent]

MAX_VALUE = 10 ** 4
MIN_VALUE = -MAX_VALUE
MAX_CONTOURS_COUNT = 5


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


def to_valid_coordinates(candidates: List[Scalar],
                         *,
                         lower_bound: int = 1,
                         upper_bound: int = int(math.sqrt(MAX_VALUE
                                                          - MIN_VALUE))
                         ) -> Tuple[Scalar, Scalar]:
    start, *rest, end = candidates
    if not (lower_bound <= end - start <= upper_bound):
        start = next((candidate
                      for candidate in rest
                      if lower_bound <= end - candidate <= upper_bound),
                     end - (upper_bound - lower_bound))
    return start, end


def pickle_round_trip(object_: Domain) -> Domain:
    return pickle.loads(pickle.dumps(object_))


def strategy_to_pairs(strategy: Strategy[Domain]
                      ) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(strategy, strategy)


def to_bound_rectangle(xs: Tuple[float, float],
                       ys: Tuple[float, float]) -> List[BoundPoint]:
    min_x, max_x = xs
    min_y, max_y = ys
    return [BoundPoint(min_x, min_y), BoundPoint(max_x, min_y),
            BoundPoint(max_x, max_y), BoundPoint(min_x, max_y)]


def to_ported_rectangle(xs: Tuple[Scalar, Scalar],
                        ys: Tuple[Scalar, Scalar]) -> List[PortedPoint]:
    min_x, max_x = xs
    min_y, max_y = ys
    return [PortedPoint(min_x, min_y), PortedPoint(max_x, min_y),
            PortedPoint(max_x, max_y), PortedPoint(min_x, max_y)]


def is_bounding_box_empty(bounding_box: Union[BoundBoundingBox,
                                              PortedBoundingBox]) -> bool:
    return not (bounding_box.x_min or bounding_box.y_min
                or bounding_box.x_max or bounding_box.y_max)


AnyContour = TypeVar('AnyContour', BoundContour, PortedContour)


def to_non_overlapping_contours_list(contours: List[AnyContour]
                                     ) -> List[AnyContour]:
    result = []
    previous_segments = []
    for contour in contours:
        segments = to_segments(contour.points)
        if all(are_non_overlapping_segments_pair(segment, previous_segment)
               for segment in segments
               for previous_segment in previous_segments):
            result.append(contour)
            previous_segments.extend(segments)
    return result


AnySweepEvent = TypeVar('AnySweepEvent', BoundSweepEvent, PortedSweepEvent)


def is_sweep_event_non_degenerate(event: AnySweepEvent) -> bool:
    return not event.segment.is_degenerate


def are_non_overlapping_sweep_events_pair(events_pair: Tuple[AnySweepEvent,
                                                             AnySweepEvent]
                                          ) -> bool:
    first_event, second_event = events_pair
    first_segment, second_segment = first_event.segment, second_event.segment
    return are_non_overlapping_segments_pair(first_segment, second_segment)


AnyPoint = TypeVar('AnyPoint', BoundPoint, PortedPoint)
AnySegment = TypeVar('AnySegment', BoundSegment, PortedSegment)


def to_segments(points: AnyPoint) -> Sequence[AnySegment]:
    if not points:
        return []
    if isinstance(points[0], BoundPoint):
        return [BoundSegment(points[index], points[(index + 1) % len(points)])
                for index in range(len(points))]
    else:
        return to_ported_segments(points)


def are_non_overlapping_segments_pair(first_segment: AnySegment,
                                      second_segment: AnySegment) -> bool:
    if isinstance(first_segment, BoundSegment):
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
    return (len(bound.contours) == len(ported.contours)
            and all(map(are_bound_ported_contours_equal,
                        bound.contours, ported.contours)))


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
