from _martinez import (EventsQueueKey,
                       SweepEvent)
from hypothesis import given

from . import strategies


@given(strategies.sweep_events)
def test_basic(event: SweepEvent) -> None:
    result = EventsQueueKey(event)

    assert result.event == event
