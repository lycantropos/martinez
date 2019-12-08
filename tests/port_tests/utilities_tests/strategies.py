from tests.strategies import (scalars_to_ported_points_triplets,
                              scalars_to_ported_segments,
                              single_precision_scalars_strategies
                              as scalars_strategies)

points_triplets = scalars_strategies.flatmap(scalars_to_ported_points_triplets)
segments = scalars_strategies.flatmap(scalars_to_ported_segments)
