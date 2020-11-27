from hypothesis import strategies

from tests.bind_tests.factories import to_bound_contours
from tests.bind_tests.hints import BoundPolygon
from tests.bind_tests.utils import (bound_operations_types,
                                    to_non_overlapping_bound_contours_list,
                                    to_non_overlapping_bound_polygons_pair)
from tests.utils import MAX_CONTOURS_COUNT

operations_types = bound_operations_types
contours = to_bound_contours()
contours_lists = (strategies.lists(contours,
                                   max_size=MAX_CONTOURS_COUNT)
                  .map(to_non_overlapping_bound_contours_list))
empty_contours_lists = strategies.builds(list)
non_empty_contours_lists = (strategies.lists(contours,
                                             min_size=1)
                            .map(to_non_overlapping_bound_contours_list))
polygons = strategies.builds(BoundPolygon, contours_lists)
empty_polygons = strategies.builds(BoundPolygon, empty_contours_lists)
non_empty_polygons = strategies.builds(BoundPolygon, non_empty_contours_lists)
polygons_pairs = (strategies.tuples(empty_polygons, non_empty_polygons) |
                  strategies.tuples(non_empty_polygons, empty_polygons) |
                  strategies.builds(to_non_overlapping_bound_polygons_pair,
                                    non_empty_polygons, non_empty_polygons))
