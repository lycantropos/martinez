from hypothesis import given

from tests.bind_tests.hints import (BoundSweepEvent,
                                    BoundSweepLineKey)
from . import strategies


@given(strategies.sweep_events)
def test_basic(event: BoundSweepEvent) -> None:
    result = BoundSweepLineKey(event)

    assert result.event == event
