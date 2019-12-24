from hypothesis import strategies

from tests.strategies import (booleans,
                              single_precision_floats as floats,
                              to_bound_with_ported_contours_pair,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_polygons_pair,
                              unsigned_integers_lists)
from tests.utils import transpose

points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)
points_lists_pairs = strategies.lists(points_pairs).map(transpose)
contours_pairs = strategies.builds(to_bound_with_ported_contours_pair,
                                   points_lists_pairs,
                                   unsigned_integers_lists,
                                   booleans)
contours_lists_pairs = strategies.lists(contours_pairs).map(transpose)
polygons_pairs = strategies.builds(to_bound_with_ported_polygons_pair,
                                   contours_lists_pairs)
