import copy

from hypothesis import given

from martinez.boolean import EdgeType, PolygonType, SweepEvent
from martinez.point import Point
from . import strategies


@given(strategies.sweep_events)
def test_shallow(sweep_event: SweepEvent) -> None:
    sweep_event = SweepEvent(True, Point(0.12739150731790999, 179769313486232),
                             None, PolygonType(1), EdgeType(3))
    sweep_event.other_event = sweep_event
    result = copy.copy(sweep_event)

    assert result is not sweep_event
    assert result == sweep_event


@given(strategies.sweep_events)
def test_deep(sweep_event: SweepEvent) -> None:
    result = copy.deepcopy(sweep_event)

    assert result is not sweep_event
    assert result == sweep_event
