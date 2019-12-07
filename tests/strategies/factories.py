from typing import (List,
                    Tuple)

from _martinez import (Contour as BoundContour,
                       Point as BoundPoint)
from hypothesis import strategies

from martinez.contour import Contour as PortedContour
from martinez.hints import Scalar
from martinez.point import Point as PortedPoint
from tests.utils import Strategy


def scalars_to_ported_points(scalars: Strategy[Scalar]
                             ) -> Strategy[PortedPoint]:
    return strategies.builds(PortedPoint, scalars, scalars)


def scalars_to_ported_points_pairs(scalars: Strategy[Scalar]
                                   ) -> Strategy[Tuple[PortedPoint,
                                                       PortedPoint]]:
    points_strategy = strategies.builds(PortedPoint, scalars, scalars)
    return strategies.tuples(points_strategy, points_strategy)


def scalars_to_ported_points_triplets(scalars: Strategy[Scalar]
                                      ) -> Strategy[Tuple[PortedPoint,
                                                          PortedPoint,
                                                          PortedPoint]]:
    points_strategy = strategies.builds(PortedPoint, scalars, scalars)
    return strategies.tuples(points_strategy, points_strategy, points_strategy)


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
