from typing import Optional

from hypothesis import given

from martinez.boolean import (Operation,
                              SweepEvent)
from . import strategies


@given(strategies.operations, strategies.sweep_events,
       strategies.maybe_nested_sweep_events)
def test_basic(operation: Operation,
               event: SweepEvent,
               previous_event: Optional[SweepEvent]) -> None:
    result = operation.compute_fields(event, previous_event)

    assert result is None


@given(strategies.operations, strategies.sweep_events,
       strategies.maybe_nested_sweep_events)
def test_properties(operation: Operation,
                    event: SweepEvent,
                    previous_event: Optional[SweepEvent]) -> None:
    operation.compute_fields(event, previous_event)

    assert event.in_result is operation.in_result(event)
