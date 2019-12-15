from hypothesis import strategies

from tests.strategies import (booleans,
                              single_precision_floats as floats,
                              to_bound_with_ported_contours_pair,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_polygons_pair,
                              unsigned_integers_lists)
from tests.utils import transpose

bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
bound_with_ported_points_lists_pairs = strategies.lists(
        bound_with_ported_points_pairs).map(transpose)
bound_with_ported_contours_pairs = strategies.builds(
        to_bound_with_ported_contours_pair,
        bound_with_ported_points_lists_pairs,
        unsigned_integers_lists,
        booleans)
bound_with_ported_contours_lists_pairs = strategies.lists(
        bound_with_ported_contours_pairs).map(transpose)
bound_with_ported_polygons_pairs = strategies.builds(
        to_bound_with_ported_polygons_pair,
        bound_with_ported_contours_lists_pairs)
