from typing import Tuple

from _martinez import (EdgeType as BoundEdgeType,
                       Point as BoundPoint,
                       PolygonType as BoundPolygonType,
                       SweepEvent as Bound)
from hypothesis import given

from martinez.boolean import (EdgeType as PortedEdgeType,
                              PolygonType as PortedPolygonType,
                              SweepEvent as Ported)
from martinez.point import Point as PortedPoint
from tests.utils import are_bound_ported_sweep_events_equal
from . import strategies


@given(strategies.booleans,
       strategies.bound_with_ported_points_pairs,
       strategies.bound_with_ported_polygons_types_pairs,
       strategies.bound_with_ported_edges_types_pairs)
def test_basic(left: bool,
               bound_with_ported_points_pair: Tuple[BoundPoint, PortedPoint],
               bound_with_ported_polygons_types_pair: Tuple[BoundPolygonType,
                                                            PortedPolygonType],
               bound_with_ported_edges_types_pair: Tuple[BoundEdgeType,
                                                         PortedEdgeType],
               ) -> None:
    bound_point, ported_point = bound_with_ported_points_pair
    (bound_polygon_type,
     ported_polygon_type) = bound_with_ported_polygons_types_pair
    bound_edge_type, ported_edge_type = bound_with_ported_edges_types_pair

    bound = Bound(left, bound_point, None, bound_polygon_type, bound_edge_type)
    ported = Ported(left, ported_point, None, ported_polygon_type,
                    ported_edge_type)

    assert are_bound_ported_sweep_events_equal(bound, ported)
