from hypothesis import strategies

from tests.strategies import (booleans,
                              single_precision_floats as floats,
                              to_bound_with_ported_contours_pair,
                              to_bound_with_ported_points_pair,
                              unsigned_integers,
                              unsigned_integers_lists)
from tests.utils import transpose

booleans = booleans
non_negative_integers = unsigned_integers
non_negative_integers_lists = unsigned_integers_lists
bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
bound_with_ported_points_lists_pairs = strategies.lists(
        bound_with_ported_points_pairs).map(transpose)
bound_with_ported_contours_pairs = strategies.builds(
        to_bound_with_ported_contours_pair,
        bound_with_ported_points_lists_pairs,
        non_negative_integers_lists,
        booleans)
