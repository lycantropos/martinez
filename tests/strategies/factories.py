from typing import (List,
                    Optional,
                    Tuple, TypeVar)

from _martinez import (Contour as BoundContour,
                       Point as BoundPoint,
                       Segment as BoundSegment,
                       SweepEvent as BoundSweepEvent)
from hypothesis import strategies

from martinez.boolean import SweepEvent as PortedSweepEvent
from martinez.contour import Contour as PortedContour
from martinez.hints import Scalar
from martinez.point import Point as PortedPoint
from martinez.segment import Segment as PortedSegment
from tests.utils import (PortedPointsPair,
                         PortedPointsTriplet,
                         Strategy, to_sweep_event_children_count)


def scalars_to_ported_points(scalars: Strategy[Scalar]
                             ) -> Strategy[PortedPoint]:
    return strategies.builds(PortedPoint, scalars, scalars)


def scalars_to_ported_points_pairs(scalars: Strategy[Scalar]
                                   ) -> Strategy[PortedPointsPair]:
    points_strategy = strategies.builds(PortedPoint, scalars, scalars)
    return strategies.tuples(points_strategy, points_strategy)


def scalars_to_ported_points_triplets(scalars: Strategy[Scalar]
                                      ) -> Strategy[PortedPointsTriplet]:
    points_strategy = strategies.builds(PortedPoint, scalars, scalars)
    return strategies.tuples(points_strategy, points_strategy, points_strategy)


def scalars_to_ported_points_lists(scalars: Strategy[Scalar],
                                   *,
                                   min_size: int = 0,
                                   max_size: Optional[int] = None
                                   ) -> Strategy[List[PortedPoint]]:
    return strategies.lists(scalars_to_ported_points(scalars),
                            min_size=min_size,
                            max_size=max_size)


def scalars_to_ported_segments(scalars: Strategy[Scalar]
                               ) -> Strategy[PortedSegment]:
    points_strategy = scalars_to_ported_points(scalars)
    return strategies.builds(PortedSegment, points_strategy, points_strategy)


def to_bound_with_ported_points_pair(x: float, y: float
                                     ) -> Tuple[BoundPoint, PortedPoint]:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_contours_pair(
        bound_with_ported_points_lists_pair: Tuple[List[BoundPoint],
                                                   List[PortedPoint]],
        holes: List[int],
        is_external: bool) -> Tuple[BoundContour, PortedContour]:
    bound_points, ported_points = bound_with_ported_points_lists_pair
    return (BoundContour(bound_points, holes, is_external),
            PortedContour(ported_points, holes, is_external))


def to_bound_with_ported_segments_pair(
        bound_with_ported_sources_pair: Tuple[BoundPoint, PortedPoint],
        bound_with_ported_targets_pair: Tuple[BoundPoint, PortedPoint]
) -> Tuple[BoundSegment, PortedSegment]:
    bound_source, ported_source = bound_with_ported_sources_pair
    bound_target, ported_target = bound_with_ported_targets_pair

    return (BoundSegment(bound_source, bound_target),
            PortedSegment(ported_source, ported_target))


AnySweepEvent = TypeVar('AnySweepEvent', PortedSweepEvent, BoundSweepEvent)


def make_cyclic(sweep_events: Strategy[AnySweepEvent]
                ) -> Strategy[AnySweepEvent]:
    return strategies.builds(to_cyclic_sweep_event,
                             sweep_events,
                             strategies.integers(),
                             strategies.integers())


def to_cyclic_sweep_event(sweep_event: AnySweepEvent,
                          source_index_seed: int,
                          destination_index_seed: int) -> AnySweepEvent:
    children_count = to_sweep_event_children_count(sweep_event) or 1
    loop_sweep_event(sweep_event,
                     source_index_seed % children_count,
                     destination_index_seed % children_count)
    return sweep_event


def loop_sweep_event(sweep_event: AnySweepEvent,
                     source_index: int, destination_index: int) -> None:
    source = destination = sweep_event
    for _ in range(source_index - 1):
        source = source.other_event
    for _ in range(destination_index):
        destination = destination.other_event
    source.other_event = destination
