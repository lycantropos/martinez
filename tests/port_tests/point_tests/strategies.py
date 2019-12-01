from typing import Tuple

from hypothesis import strategies

from martinez.hints import Scalar
from martinez.point import Point
from tests.strategies import scalars_strategies
from tests.utils import Strategy


def scalars_to_pairs(scalars: Strategy[Scalar]
                     ) -> Strategy[Tuple[Scalar, Scalar]]:
    return strategies.tuples(scalars, scalars)


scalars_pairs = scalars_strategies.flatmap(scalars_to_pairs)


def scalars_to_points(scalars: Strategy[Scalar]) -> Strategy[Point]:
    return strategies.builds(Point, scalars, scalars)


points = scalars_strategies.flatmap(scalars_to_points)


def scalars_to_points_pairs(scalars: Strategy[Scalar]
                            ) -> Strategy[Tuple[Point, Point]]:
    points_strategy = strategies.builds(Point, scalars, scalars)
    return strategies.tuples(points_strategy, points_strategy)


points_pairs = scalars_strategies.flatmap(scalars_to_points_pairs)


def scalars_to_points_triplets(scalars: Strategy[Scalar]
                               ) -> Strategy[Tuple[Point, Point, Point]]:
    points_strategy = strategies.builds(Point, scalars, scalars)
    return strategies.tuples(points_strategy, points_strategy, points_strategy)


points_triplets = scalars_strategies.flatmap(scalars_to_points_triplets)
