from typing import Optional

from hypothesis import given

from martinez.boolean import (EdgeType,
                              PolygonType,
                              SweepEvent)
from martinez.point import Point
from . import strategies


@given(strategies.booleans, strategies.points, strategies.maybe_sweep_events,
       strategies.polygons_types, strategies.edges_types)
def test_basic(left: bool, point: Point,
               other_event: Optional[SweepEvent],
               polygon_type: PolygonType,
               edge_type: EdgeType) -> None:
    result = SweepEvent(left, point, other_event,
                        polygon_type, edge_type)

    assert result.left is left
    assert result.point == point
    assert result.other_event is other_event
    assert result.polygon_type == polygon_type
    assert result.edge_type == edge_type
