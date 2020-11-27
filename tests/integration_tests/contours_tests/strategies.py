from hypothesis import strategies

from tests.integration_tests.factories import (
    to_bound_with_ported_contours_pair,
    to_bound_with_ported_points_pair)
from tests.strategies import (booleans,
                              single_precision_floats as floats,
                              unsigned_integers,
                              unsigned_integers_lists)
from tests.utils import transpose

booleans = booleans
non_negative_integers = unsigned_integers
non_negative_integers_lists = unsigned_integers_lists
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)
points_lists_pairs = strategies.lists(points_pairs).map(transpose)
contours_pairs = strategies.builds(to_bound_with_ported_contours_pair,
                                   points_lists_pairs,
                                   non_negative_integers_lists,
                                   booleans)
