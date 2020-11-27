from itertools import repeat

from hypothesis import strategies

from tests.strategies import (single_precision_floats as floats)
from tests.integration_tests.factories import to_bound_with_ported_points_pair, \
    to_bound_with_ported_segments_pair
from tests.utils import (to_pairs,
                         transpose)

points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)
points_triplets_pairs = (strategies.tuples(*repeat(points_pairs, 3))
                         .map(transpose))
segments_pairs = strategies.builds(to_bound_with_ported_segments_pair,
                                   points_pairs, points_pairs)
segments_pairs_pairs = to_pairs(segments_pairs).map(transpose)
