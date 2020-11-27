from hypothesis import given

from tests.port_tests.hints import (PortedSweepEvent,
                                    PortedSweepLineKey)
from . import strategies


@given(strategies.sweep_events)
def test_basic(event: PortedSweepEvent) -> None:
    result = PortedSweepLineKey(event)

    assert result.event == event
