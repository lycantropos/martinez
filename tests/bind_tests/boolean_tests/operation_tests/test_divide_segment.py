from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundPoint,
                                    BoundSweepEvent)
from . import strategies


@given(strategies.operations, strategies.double_nested_sweep_events,
       strategies.points)
def test_basic(operation: BoundOperation,
               event: BoundSweepEvent,
               point: BoundPoint) -> None:
    result = operation.divide_segment(event, point)

    assert result is None


@given(strategies.operations, strategies.double_nested_sweep_events,
       strategies.points)
def test_events(operation: BoundOperation,
                event: BoundSweepEvent,
                point: BoundPoint) -> None:
    events_before = operation.events

    operation.divide_segment(event, point)

    events_after = operation.events

    assert isinstance(events_before, list)
    assert isinstance(events_after, list)
    assert not events_before
    assert len(events_after) == 2
    assert all(isinstance(event, BoundSweepEvent) for event in events_after)
