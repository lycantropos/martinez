from hypothesis import given

from tests.port_tests.hints import (PortedEventsQueueKey,
                                    PortedSweepEvent)
from . import strategies


@given(strategies.sweep_events)
def test_basic(event: PortedSweepEvent) -> None:
    result = PortedEventsQueueKey(event)

    assert result.event == event
