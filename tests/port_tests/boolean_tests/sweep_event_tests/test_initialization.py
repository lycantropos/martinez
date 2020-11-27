from typing import Optional

from hypothesis import given

from tests.port_tests.hints import (PortedEdgeType,
                                    PortedPoint,
                                    PortedPolygonType,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.booleans, strategies.points, strategies.maybe_sweep_events,
       strategies.polygons_types, strategies.edges_types, strategies.booleans,
       strategies.booleans, strategies.booleans, strategies.booleans,
       strategies.non_negative_integers, strategies.non_negative_integers,
       strategies.maybe_sweep_events)
def test_basic(is_left: bool,
               point: PortedPoint,
               other_event: Optional[PortedSweepEvent],
               polygon_type: PortedPolygonType,
               edge_type: PortedEdgeType,
               in_out: bool,
               other_in_out: bool,
               in_result: bool,
               result_in_out: bool,
               position: int,
               contour_id: int,
               prev_in_result_event: Optional[PortedSweepEvent]) -> None:
    result = PortedSweepEvent(is_left, point, other_event, polygon_type,
                              edge_type, in_out, other_in_out, in_result,
                              result_in_out, position, contour_id,
                              prev_in_result_event)

    assert result.is_left is is_left
    assert result.point == point
    assert result.other_event is other_event
    assert result.polygon_type == polygon_type
    assert result.edge_type == edge_type
    assert result.in_out is in_out
    assert result.other_in_out is other_in_out
    assert result.in_result is in_result
    assert result.result_in_out is result_in_out
    assert result.position == position
    assert result.contour_id == contour_id
    assert result.prev_in_result_event is prev_in_result_event
