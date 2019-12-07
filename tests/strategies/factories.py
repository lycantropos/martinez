from typing import (List,
                    Optional,
                    Tuple)

from _martinez import (Contour as BoundContour,
                       Point as BoundPoint,
                       Segment as BoundSegment)
from hypothesis import strategies

from martinez.contour import Contour as PortedContour
from martinez.hints import Scalar
from martinez.point import Point as PortedPoint
from martinez.segment import Segment as PortedSegment
from tests.utils import (PortedPointsPair,
                         PortedPointsTriplet,
                         Strategy)


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
