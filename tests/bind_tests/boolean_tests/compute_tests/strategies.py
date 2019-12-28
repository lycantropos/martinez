from _martinez import Polygon
from hypothesis import strategies

from tests.strategies import (bound_operations_types,
                              to_bound_contours)
from tests.utils import (MAX_CONTOURS_COUNT,
                         to_non_overlapping_bound_polygons_pair,
                         to_non_overlapping_contours_list)

operations_types = bound_operations_types
contours = to_bound_contours()
contours_lists = (strategies.lists(contours,
                                   max_size=MAX_CONTOURS_COUNT)
                  .map(to_non_overlapping_contours_list))
empty_contours_lists = strategies.builds(list)
non_empty_contours_lists = (strategies.lists(contours,
                                             min_size=1)
                            .map(to_non_overlapping_contours_list))
polygons = strategies.builds(Polygon, contours_lists)
empty_polygons = strategies.builds(Polygon, empty_contours_lists)
non_empty_polygons = strategies.builds(Polygon, non_empty_contours_lists)
polygons_pairs = (strategies.tuples(empty_polygons, non_empty_polygons) |
                  strategies.tuples(non_empty_polygons, empty_polygons) |
                  strategies.builds(to_non_overlapping_bound_polygons_pair,
                                    non_empty_polygons, non_empty_polygons))
