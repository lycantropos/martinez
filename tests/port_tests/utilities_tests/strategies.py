from tests.port_tests.factories import (scalars_to_ported_points_triplets,
                                        scalars_to_ported_segments)
from tests.strategies import (single_precision_scalars_strategies
                              as scalars_strategies)
from tests.utils import (identity,
                         to_pairs)

points_triplets = scalars_strategies.flatmap(scalars_to_ported_points_triplets)
segments_strategies = scalars_strategies.map(scalars_to_ported_segments)
segments = segments_strategies.flatmap(identity)
segments_pairs = segments_strategies.flatmap(to_pairs)
