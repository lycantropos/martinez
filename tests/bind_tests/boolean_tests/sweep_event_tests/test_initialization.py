from typing import Optional

from _martinez import (EdgeType,
                       Point,
                       PolygonType,
                       SweepEvent)
from hypothesis import given

from . import strategies


@given(strategies.booleans, strategies.points, strategies.maybe_sweep_events,
       strategies.polygons_types, strategies.edges_types,
       strategies.booleans, strategies.booleans)
def test_basic(is_left: bool, point: Point, other_event: Optional[SweepEvent],
               polygon_type: PolygonType, edge_type: EdgeType, in_out: bool,
               other_in_out: bool) -> None:
    result = SweepEvent(is_left, point, other_event, polygon_type, edge_type,
                        in_out, other_in_out)

    assert result.is_left is is_left
    assert result.point == point
    assert result.other_event is other_event
    assert result.polygon_type == polygon_type
    assert result.edge_type == edge_type
    assert result.in_out is in_out
    assert result.other_in_out is other_in_out
