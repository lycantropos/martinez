from typing import List

from hypothesis import given

from martinez.boolean import (Operation,
                              SweepEvent)
from . import strategies


@given(strategies.nested_sweep_events_lists)
def test_basic(events: List[SweepEvent]) -> None:
    result = Operation.collect_events(events)

    assert isinstance(result, list)
    assert all(isinstance(element, SweepEvent) for element in result)
