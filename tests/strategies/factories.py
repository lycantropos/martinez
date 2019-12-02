from typing import Tuple

from _martinez import Point as BoundPoint
from hypothesis import strategies

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


def to_bound_with_ported_points_pair(x: float, y: float
                                     ) -> Tuple[BoundPoint, PortedPoint]:
    return BoundPoint(x, y), PortedPoint(x, y)
