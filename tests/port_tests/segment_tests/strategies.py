from tests.strategies import (scalars_strategies,
                              scalars_to_ported_points_pairs,
                              scalars_to_ported_segments)

points_pairs = scalars_strategies.flatmap(scalars_to_ported_points_pairs)
segments = scalars_strategies.flatmap(scalars_to_ported_segments)
