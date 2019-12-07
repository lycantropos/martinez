from hypothesis import strategies

from tests.strategies import (floats,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_segments_pair)

floats = floats
bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
bound_with_ported_segments_pairs = strategies.builds(
        to_bound_with_ported_segments_pair,
        bound_with_ported_points_pairs, bound_with_ported_points_pairs)
