from tests.strategies import (scalars_strategies)
from tests.port_tests.factories import scalars_to_ported_points_pairs, \
    scalars_to_ported_segments
from tests.utils import (identity,
                         to_pairs,
                         to_triplets)

points_pairs = scalars_strategies.flatmap(scalars_to_ported_points_pairs)
segments_strategies = scalars_strategies.map(scalars_to_ported_segments)
segments = segments_strategies.flatmap(identity)
segments_pairs = segments_strategies.flatmap(to_pairs)
segments_triplets = segments_strategies.flatmap(to_triplets)
