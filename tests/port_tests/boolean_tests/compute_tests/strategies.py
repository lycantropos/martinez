from functools import partial

from hypothesis import strategies

from martinez.polygon import Polygon
from tests.strategies import (ported_operations_types,
                              scalars_strategies,
                              scalars_to_ported_polygons)
from tests.utils import to_non_overlapping_ported_polygons_pair

operations_types = ported_operations_types
empty_polygons = strategies.builds(Polygon, strategies.builds(list))
polygons = scalars_strategies.flatmap(scalars_to_ported_polygons)
non_empty_polygons = (scalars_strategies
                      .flatmap(partial(scalars_to_ported_polygons,
                                       min_size=1)))
polygons_pairs = (strategies.tuples(empty_polygons, non_empty_polygons) |
                  strategies.tuples(non_empty_polygons, empty_polygons) |
                  strategies.builds(to_non_overlapping_ported_polygons_pair,
                                    non_empty_polygons, non_empty_polygons))
