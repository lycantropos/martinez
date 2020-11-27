from typing import List

from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundSweepEvent)
from . import strategies


@given(strategies.nested_sweep_events_lists)
def test_basic(events: List[BoundSweepEvent]) -> None:
    result = BoundOperation.collect_events(events)

    assert isinstance(result, list)
    assert all(isinstance(element, BoundSweepEvent) for element in result)
