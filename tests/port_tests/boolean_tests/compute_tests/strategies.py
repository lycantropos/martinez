from functools import partial

from hypothesis import strategies

from tests.port_tests.factories import scalars_to_ported_polygons
from tests.port_tests.hints import PortedPolygon
from tests.port_tests.utils import (ported_operations_types,
                                    to_non_overlapping_ported_polygons_pair)
from tests.strategies import scalars_strategies
from tests.utils import (identity,
                         pack,
                         to_pairs)

operations_types = ported_operations_types
empty_polygons = strategies.builds(PortedPolygon, strategies.builds(list))
polygons = scalars_strategies.flatmap(scalars_to_ported_polygons)
non_empty_polygons_strategies = (scalars_strategies
                                 .map(partial(scalars_to_ported_polygons,
                                              min_size=1)))
non_empty_polygons = non_empty_polygons_strategies.flatmap(identity)
polygons_pairs = (strategies.tuples(empty_polygons, non_empty_polygons) |
                  strategies.tuples(non_empty_polygons, empty_polygons) |
                  non_empty_polygons_strategies
                  .flatmap(to_pairs)
                  .map(pack(to_non_overlapping_ported_polygons_pair)))
