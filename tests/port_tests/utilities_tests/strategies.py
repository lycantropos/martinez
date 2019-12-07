from tests.strategies import (scalars_strategies,
                              scalars_to_ported_points_triplets)

points_triplets = scalars_strategies.flatmap(scalars_to_ported_points_triplets)
