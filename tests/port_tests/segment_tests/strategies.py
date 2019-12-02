from tests.strategies import (scalars_strategies,
                              scalars_to_points_pairs)

points_pairs = scalars_strategies.flatmap(scalars_to_points_pairs)
