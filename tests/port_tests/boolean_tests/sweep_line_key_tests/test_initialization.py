from hypothesis import given

from martinez.boolean import (SweepEvent,
                              SweepLineKey)
from . import strategies


@given(strategies.sweep_events)
def test_basic(event: SweepEvent) -> None:
    result = SweepLineKey(event)

    assert result.event == event
