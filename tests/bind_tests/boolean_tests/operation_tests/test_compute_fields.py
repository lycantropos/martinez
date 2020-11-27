from typing import Optional

from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from . import strategies


@given(strategies.operations, strategies.sweep_events,
       strategies.maybe_nested_sweep_events)
def test_basic(operation: BoundOperation,
               event: BoundSweepEvent,
               previous_event: Optional[BoundSweepEvent]) -> None:
    result = operation.compute_fields(event, previous_event)

    assert result is None


@given(strategies.operations, strategies.sweep_events,
       strategies.maybe_nested_sweep_events)
def test_properties(operation: BoundOperation,
                    event: BoundSweepEvent,
                    previous_event: Optional[BoundSweepEvent]) -> None:
    operation.compute_fields(event, previous_event)

    assert event.in_result is operation.in_result(event)
