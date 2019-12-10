from _martinez import (EdgeType as BoundEdgeType,
                       PolygonType as BoundPolygonType)
from hypothesis import strategies

from martinez.boolean import (EdgeType as PortedEdgeType,
                              PolygonType as PortedPolygonType)
from tests.strategies import (booleans,
                              single_precision_floats as floats,
                              to_bound_with_ported_points_pair)

booleans = booleans
bound_with_ported_points_pairs = strategies.builds(
        to_bound_with_ported_points_pair, floats, floats)
bound_with_ported_polygons_types_pairs = strategies.sampled_from(
        [(BoundPolygonType.__members__[name],
          PortedPolygonType.__members__[name])
         for name in (BoundPolygonType.__members__.keys() &
                      PortedPolygonType.__members__.keys())])
bound_with_ported_edges_types_pairs = strategies.sampled_from(
        [(BoundEdgeType.__members__[name],
          PortedEdgeType.__members__[name])
         for name in (BoundEdgeType.__members__.keys() &
                      PortedEdgeType.__members__.keys())])
