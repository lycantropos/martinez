from typing import Tuple

from hypothesis import strategies

from tests.bind_tests.hints import BoundPolygon
from tests.bind_tests.utils import to_non_overlapping_bound_polygons_pair
from tests.integration_tests.factories import (
    to_bound_with_ported_contours_pair,
    to_bound_with_ported_contours_vertices_pair,
    to_bound_with_ported_polygons_pair)
from tests.integration_tests.utils import (
    bound_with_ported_operations_types_pairs,
    to_non_overlapping_contours_lists)
from tests.port_tests.hints import PortedPolygon
from tests.port_tests.utils import to_non_overlapping_ported_polygons_pair
from tests.strategies import single_precision_floats as floats
from tests.utils import (MAX_CONTOURS_COUNT,
                         to_pairs,
                         transpose)

operations_types_pairs = bound_with_ported_operations_types_pairs
contours_vertices_pairs = to_bound_with_ported_contours_vertices_pair(floats)
contours_pairs = strategies.builds(to_bound_with_ported_contours_pair,
                                   contours_vertices_pairs,
                                   strategies.builds(list),
                                   strategies.just(True))
contours_lists_pairs = (strategies.lists(contours_pairs,
                                         max_size=MAX_CONTOURS_COUNT)
                        .map(transpose)
                        .map(to_non_overlapping_contours_lists))
empty_contours_lists_pairs = to_pairs(strategies.builds(list))
non_empty_contours_lists_pairs = (strategies.lists(contours_pairs,
                                                   min_size=1,
                                                   max_size=1)
                                  .map(transpose)
                                  .map(to_non_overlapping_contours_lists))
polygons_pairs = strategies.builds(to_bound_with_ported_polygons_pair,
                                   contours_lists_pairs)
empty_polygons_pairs = strategies.builds(to_bound_with_ported_polygons_pair,
                                         empty_contours_lists_pairs)
non_empty_polygons_pairs = strategies.builds(
        to_bound_with_ported_polygons_pair,
        non_empty_contours_lists_pairs)


def to_non_overlapping_polygons_pairs(first_pairs_pair: Tuple[BoundPolygon,
                                                              PortedPolygon],
                                      second_pairs_pair: Tuple[BoundPolygon,
                                                               PortedPolygon]
                                      ) -> Tuple[Tuple[BoundPolygon,
                                                       PortedPolygon],
                                                 Tuple[BoundPolygon,
                                                       PortedPolygon]]:
    first_bound_polygon, first_ported_polygon = first_pairs_pair
    second_bound_polygon, second_ported_polygon = second_pairs_pair
    bound_polygons_pair = to_non_overlapping_bound_polygons_pair(
            first_bound_polygon,
            second_bound_polygon)
    ported_polygons_pair = to_non_overlapping_ported_polygons_pair(
            first_ported_polygon,
            second_ported_polygon)
    return transpose([bound_polygons_pair, ported_polygons_pair])


polygons_pairs_pairs = (strategies.tuples(empty_polygons_pairs,
                                          non_empty_polygons_pairs)
                        | strategies.tuples(non_empty_polygons_pairs,
                                            empty_polygons_pairs)
                        | strategies.builds(to_non_overlapping_polygons_pairs,
                                            non_empty_polygons_pairs,
                                            non_empty_polygons_pairs))
