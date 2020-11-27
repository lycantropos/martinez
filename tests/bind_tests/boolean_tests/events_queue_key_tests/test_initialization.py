from hypothesis import given

from tests.bind_tests.hints import (BoundEventsQueueKey,
                                    BoundSweepEvent)
from . import strategies


@given(strategies.sweep_events)
def test_basic(event: BoundSweepEvent) -> None:
    result = BoundEventsQueueKey(event)

    assert result.event == event
