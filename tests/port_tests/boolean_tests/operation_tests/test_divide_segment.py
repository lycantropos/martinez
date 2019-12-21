from hypothesis import given

from martinez.boolean import (Operation,
                              SweepEvent)
from martinez.point import Point
from . import strategies


@given(strategies.operations, strategies.nested_sweep_events,
       strategies.points)
def test_basic(operation: Operation, event: SweepEvent, point: Point) -> None:
    result = operation.divide_segment(event, point)

    assert result is None


@given(strategies.operations, strategies.nested_sweep_events,
       strategies.points)
def test_events(operation: Operation, event: SweepEvent, point: Point) -> None:
    events_before = operation.events

    operation.divide_segment(event, point)

    events_after = operation.events

    assert isinstance(events_before, list)
    assert isinstance(events_after, list)
    assert not events_before
    assert len(events_after) == 2
    assert all(isinstance(event, SweepEvent) for event in events_after)
