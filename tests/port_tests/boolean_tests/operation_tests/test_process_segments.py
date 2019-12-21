from hypothesis import given

from martinez.boolean import (Operation,
                              SweepEvent)
from . import strategies


@given(strategies.operations)
def test_basic(operation: Operation) -> None:
    result = operation.process_segments()

    assert result is None


@given(strategies.operations)
def test_events(operation: Operation) -> None:
    events_before = operation.events

    operation.process_segments()

    events_after = operation.events

    assert isinstance(events_before, list)
    assert isinstance(events_after, list)
    assert not events_before
    assert not len(events_after) % 2
    assert all(isinstance(event, SweepEvent) for event in events_after)
