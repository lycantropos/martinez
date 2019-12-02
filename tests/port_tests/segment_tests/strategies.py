from hypothesis import strategies

from martinez.hints import Scalar
from martinez.segment import Segment
from tests.strategies import (scalars_strategies,
                              scalars_to_ported_points,
                              scalars_to_ported_points_pairs)
from tests.utils import Strategy

points_pairs = scalars_strategies.flatmap(scalars_to_ported_points_pairs)


def scalars_to_segments(scalars: Strategy[Scalar]) -> Strategy[Segment]:
    points_strategy = scalars_to_ported_points(scalars)
    return strategies.builds(Segment, points_strategy, points_strategy)


segments = scalars_strategies.flatmap(scalars_to_segments)
