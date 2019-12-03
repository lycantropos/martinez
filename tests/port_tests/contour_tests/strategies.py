from hypothesis import strategies

from tests.strategies import (scalars_strategies,
                              scalars_to_ported_points)

points_lists = strategies.lists(scalars_strategies
                                .flatmap(scalars_to_ported_points))
non_negative_integers_lists = strategies.lists(strategies.integers(0))
booleans = strategies.booleans()
