from typing import (Optional,
                    Tuple)

from hypothesis import given

from martinez.point import Point as PortedPoint
from tests.bind_tests.hints import (BoundEdgeType,
                                    BoundPoint,
                                    BoundPolygonType,
                                    BoundSweepEvent)
from tests.integration_tests.utils import are_bound_ported_sweep_events_equal
from tests.port_tests.hints import (PortedEdgeType,
                                    PortedPolygonType,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.booleans, strategies.points_pairs,
       strategies.maybe_sweep_events_pairs, strategies.polygons_types_pairs,
       strategies.edges_types_pairs, strategies.booleans, strategies.booleans,
       strategies.booleans, strategies.booleans, strategies.unsigned_integers,
       strategies.unsigned_integers, strategies.maybe_sweep_events_pairs)
def test_basic(is_left: bool,
               points_pair: Tuple[BoundPoint, PortedPoint],
               other_events_pair: Tuple[Optional[BoundSweepEvent],
                                        Optional[PortedSweepEvent]],
               polygons_types_pair: Tuple[BoundPolygonType, PortedPolygonType],
               edges_types_pair: Tuple[BoundEdgeType, PortedEdgeType],
               in_out: bool,
               other_in_out: bool,
               in_result: bool,
               result_in_out: bool,
               position: int,
               contour_id: int,
               prev_in_result_events_pair: Tuple[Optional[BoundSweepEvent],
                                                 Optional[PortedSweepEvent]]
               ) -> None:
    bound_point, ported_point = points_pair
    bound_other_event, ported_other_event = other_events_pair
    bound_polygon_type, ported_polygon_type = polygons_types_pair
    bound_edge_type, ported_edge_type = edges_types_pair
    (bound_prev_in_result_event,
     ported_prev_in_result_event) = prev_in_result_events_pair

    bound = BoundSweepEvent(is_left, bound_point, bound_other_event,
                            bound_polygon_type, bound_edge_type, in_out,
                            other_in_out, in_result, result_in_out, position,
                            contour_id, bound_prev_in_result_event)
    ported = PortedSweepEvent(is_left, ported_point, ported_other_event,
                              ported_polygon_type, ported_edge_type, in_out,
                              other_in_out, in_result, result_in_out, position,
                              contour_id, ported_prev_in_result_event)

    assert are_bound_ported_sweep_events_equal(bound, ported)
