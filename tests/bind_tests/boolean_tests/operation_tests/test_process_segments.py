from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from . import strategies


@given(strategies.operations)
def test_basic(operation: BoundOperation) -> None:
    result = operation.process_segments()

    assert result is None


@given(strategies.operations)
def test_events(operation: BoundOperation) -> None:
    events_before = operation.events

    operation.process_segments()

    events_after = operation.events

    assert isinstance(events_before, list)
    assert isinstance(events_after, list)
    assert not events_before
    assert not len(events_after) % 2
    assert all(isinstance(event, BoundSweepEvent) for event in events_after)
