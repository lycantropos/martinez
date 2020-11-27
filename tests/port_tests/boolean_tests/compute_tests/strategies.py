from functools import partial

from hypothesis import strategies

from martinez.polygon import Polygon
from tests.strategies import (ported_operations_types,
                              scalars_strategies)
from tests.port_tests.factories import scalars_to_ported_polygons
from tests.utils import (identity,
                         pack,
                         to_pairs)
from tests.port_tests.utils import to_non_overlapping_ported_polygons_pair

operations_types = ported_operations_types
empty_polygons = strategies.builds(Polygon, strategies.builds(list))
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
