from itertools import repeat

from hypothesis import strategies

from tests.strategies import (single_precision_floats as floats,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_segments_pair)
from tests.utils import transpose

bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
bound_with_ported_points_triplets_pairs = strategies.tuples(
        *repeat(bound_with_ported_points_pairs, 3)).map(transpose)
bound_with_ported_segments_pairs = strategies.builds(
        to_bound_with_ported_segments_pair,
        bound_with_ported_points_pairs, bound_with_ported_points_pairs)
bound_with_ported_segments_pairs_pairs = strategies.tuples(
        *repeat(bound_with_ported_segments_pairs, 2)).map(transpose)
