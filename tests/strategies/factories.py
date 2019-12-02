from typing import Tuple

from hypothesis import strategies

from martinez.hints import Scalar
from martinez.point import Point
from tests.utils import Strategy


def scalars_to_points_pairs(scalars: Strategy[Scalar]
                            ) -> Strategy[Tuple[Point, Point]]:
    points_strategy = strategies.builds(Point, scalars, scalars)
    return strategies.tuples(points_strategy, points_strategy)
